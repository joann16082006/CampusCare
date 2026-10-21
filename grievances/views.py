from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import GrievanceForm
from .models import Grievance, GrievanceHistory
from accounts.decorators import role_required


@role_required('STUDENT')
def submit_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.student = request.user
            grievance.save()
            return redirect('my_grievances')
    else:
        form = GrievanceForm()

    return render(request, 'grievances/submit_grievance.html', {'form': form})


@role_required('STUDENT')
def my_grievances(request):
    grievances = Grievance.objects.filter(
        student=request.user
    ).order_by('-created_at')
    return render(
        request,
        'grievances/my_grievances.html',
        {'grievances': grievances}
    )


@role_required('STAFF')
def staff_grievances(request):
    grievances = Grievance.objects.select_related(
        'student'
    ).order_by('-created_at')
    return render(
        request,
        'grievances/staff_grievances.html',
        {'grievances': grievances}
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
            messages.info(request, 'The grievance already has that status.')

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
        {'grievance': grievance, 'history': history}
    )


@role_required('STUDENT')
def edit_grievance(request, pk):
    grievance = get_object_or_404(
        Grievance,
        pk=pk,
        student=request.user
    )
    if request.method == 'POST':
        form = GrievanceForm(request.POST, instance=grievance)
        if form.is_valid():
            form.save()
            return redirect('my_grievances')
    else:
        form = GrievanceForm(instance=grievance)

    return render(
        request,
        'grievances/edit_grievance.html',
        {'form': form, 'grievance': grievance}
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
        return redirect('my_grievances')

    return render(
        request,
        'grievances/delete_grievance.html',
        {'grievance': grievance}
    )
