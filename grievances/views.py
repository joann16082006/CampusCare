from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import GrievanceForm
from .models import Grievance


@login_required
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


@login_required
def my_grievances(request):
    grievances = Grievance.objects.filter(
        student=request.user
    ).order_by('-created_at')

    return render(
        request,
        'grievances/my_grievances.html',
        {'grievances': grievances}
    )


@login_required
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


@login_required
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
