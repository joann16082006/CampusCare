from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import GrievanceForm
from .models import Grievance, GrievanceHistory
from accounts.decorators import role_required


# ---------------- STUDENT: Member 3 (CRUD) + Member 5 (search) ----------------

@role_required('STUDENT')
def submit_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST)

        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.student = request.user
            grievance.save()

            messages.success(
                request,
                'Grievance submitted successfully!'
            )
            return redirect('my_grievances')
    else:
        form = GrievanceForm()

    return render(
        request,
        'grievances/submit_grievance.html',
        {'form': form}
    )


@role_required('STUDENT')
def my_grievances(request):
    grievances = Grievance.objects.filter(
        student=request.user
    ).order_by('-created_at')

    # Get search and filter values
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')

    # Search by title or description
    if q:
        grievances = grievances.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    # Filter by status
    if status:
        grievances = grievances.filter(status=status)

    # Filter by category
    if category:
        grievances = grievances.filter(category=category)

    # Pagination: 5 per page
    paginator = Paginator(grievances, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'grievances/my_grievances.html',
        {
            'page_obj': page_obj,
            'q': q,
            'status': status,
            'category': category,
            'status_choices': Grievance.STATUS_CHOICES,
            'category_choices': Grievance.CATEGORY_CHOICES,
        }
    )


@role_required('STUDENT')
def edit_grievance(request, pk):
    grievance = get_object_or_404(
        Grievance,
        pk=pk,
        student=request.user
    )

    if request.method == 'POST':
        form = GrievanceForm(
            request.POST,
            instance=grievance
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Grievance updated successfully!'
            )
            return redirect('my_grievances')
    else:
        form = GrievanceForm(instance=grievance)

    return render(
        request,
        'grievances/edit_grievance.html',
        {
            'form': form,
            'grievance': grievance
        }
    )


@role_required('STUDENT')
def delete_grievance(request, pk):
    grievance = get_object_or_404(
        Grievance,
        pk=pk,
        student=request.user
    )

    if request.method == 'POST':
        grievance.delete()

        messages.success(
            request,
            'Grievance deleted successfully!'
        )
        return redirect('my_grievances')

    return render(
        request,
        'grievances/delete_grievance.html',
        {'grievance': grievance}
    )


# ---------------- STAFF: Member 4 (dashboard + status history) ----------------

@role_required('STAFF')
def staff_grievances(request):
    grievances = Grievance.objects.select_related(
        'student'
    ).order_by('-created_at')

    return render(
        request,
        'grievances/staff_grievances.html',
        {
            'grievances': grievances,
            'status_choices': Grievance.STATUS_CHOICES,
        }
    )


@role_required('STAFF')
@require_POST
def update_grievance_status(request, grievance_id):
    with transaction.atomic():
        grievance = get_object_or_404(
            Grievance.objects.select_for_update(),
            pk=grievance_id
        )

        new_status = request.POST.get('status', '')
        allowed_statuses = dict(Grievance.STATUS_CHOICES)

        if new_status not in allowed_statuses:
            messages.error(request, 'Please select a valid status.')
            return redirect('staff_grievances')

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

            messages.success(
                request,
                f'Status updated to {allowed_statuses[new_status]}.'
            )
        else:
            messages.info(
                request,
                'The grievance already has that status.'
            )

    return redirect('staff_grievances')


@role_required('STAFF')
def grievance_history(request, grievance_id):
    grievance = get_object_or_404(Grievance, pk=grievance_id)

    history = grievance.history.select_related(
        'staff'
    ).order_by('-changed_at')

    return render(
        request,
        'grievances/grievance_history.html',
        {
            'grievance': grievance,
            'history': history,
        }
    )
