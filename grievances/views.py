from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import GrievanceForm
from .models import Grievance, GrievanceHistory
from accounts.decorators import role_required


# ---------------- STUDENT ----------------

@role_required('STUDENT')
def submit_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.student = request.user
            grievance.save()
            messages.success(request, 'Grievance submitted successfully!')
            return redirect('my_grievances')
    else:
        form = GrievanceForm()

    return render(request, 'grievances/submit_grievance.html', {'form': form})


@role_required('STUDENT')
def my_grievances(request):
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')

    if q:
        grievances = grievances.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status:
        grievances = grievances.filter(status=status)
    if category:
        grievances = grievances.filter(category=category)

    page_obj = Paginator(grievances, 5).get_page(request.GET.get('page'))

    return render(request, 'grievances/my_grievances.html', {
        'page_obj': page_obj,
        'q': q,
        'status': status,
        'category': category,
        'status_choices': Grievance.STATUS_CHOICES,
        'category_choices': Grievance.CATEGORY_CHOICES,
    })


@role_required('STUDENT')
def edit_grievance(request, pk):
    grievance = get_object_or_404(Grievance, pk=pk, student=request.user)

    if request.method == 'POST':
        form = GrievanceForm(request.POST, instance=grievance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grievance updated successfully!')
            return redirect('grievance_detail', pk=grievance.pk)
    else:
        form = GrievanceForm(instance=grievance)

    return render(request, 'grievances/edit_grievance.html', {'form': form, 'grievance': grievance})


@role_required('STUDENT')
def delete_grievance(request, pk):
    grievance = get_object_or_404(Grievance, pk=pk, student=request.user)

    if request.method == 'POST':
        grievance.delete()
        messages.success(request, 'Grievance deleted successfully!')
        return redirect('my_grievances')

    return render(request, 'grievances/delete_grievance.html', {'grievance': grievance})

# ---------------- DETAIL (student: own only, staff: any) ----------------

@role_required('STUDENT', 'STAFF', 'ADMIN')
def grievance_detail(request, pk):
    if request.user.profile.role == 'STUDENT':
        grievance = get_object_or_404(Grievance, pk=pk, student=request.user)
    else:
        grievance = get_object_or_404(Grievance.objects.select_related('student'), pk=pk)
        # Staff opened it, so it is no longer "new"
        if not grievance.staff_seen:
            grievance.staff_seen = True
            grievance.save(update_fields=['staff_seen'])

    history = grievance.history.select_related('staff').order_by('-changed_at')

    return render(request, 'grievances/grievance_detail.html', {
        'grievance': grievance,
        'history': history,
        'status_choices': Grievance.STATUS_CHOICES,
    })


# ---------------- STAFF ----------------

@role_required('STAFF')
def staff_grievances(request):
    # Staff opened the list, so every grievance is now "seen"
    Grievance.objects.filter(staff_seen=False).update(staff_seen=True)

    grievances = Grievance.objects.select_related('student').order_by('-created_at')

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')

    if q:
        grievances = grievances.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(student__username__icontains=q)
        )
    if status:
        grievances = grievances.filter(status=status)

    page_obj = Paginator(grievances, 10).get_page(request.GET.get('page'))

    return render(request, 'grievances/staff_grievances.html', {
        'page_obj': page_obj,
        'q': q,
        'status': status,
        'status_choices': Grievance.STATUS_CHOICES,
    })


@role_required('STAFF')
@require_POST
def update_grievance_status(request, grievance_id):
    with transaction.atomic():
        grievance = get_object_or_404(Grievance.objects.select_for_update(), pk=grievance_id)

        new_status = request.POST.get('status', '')
        allowed_statuses = dict(Grievance.STATUS_CHOICES)

        if new_status not in allowed_statuses:
            messages.error(request, 'Please select a valid status.')
        else:
            previous_status = grievance.status
            if new_status != previous_status:
                grievance.status = new_status
                grievance.save(update_fields=['status'])
                GrievanceHistory.objects.create(
                    grievance=grievance,
                    staff=request.user,
                    previous_status=previous_status,
                    new_status=new_status,
                )
                messages.success(request, f'Status updated to {allowed_statuses[new_status]}.')
            else:
                messages.info(request, 'The grievance already has that status.')

    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('staff_grievances')


@role_required('STAFF')
def grievance_history(request, grievance_id):
    return redirect('grievance_detail', pk=grievance_id)