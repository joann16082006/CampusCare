
from django.shortcuts import render, redirect, get_object_or_404
from .forms import GrievanceForm
from .models import Grievance
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

    return render(
        request,
        'grievances/my_grievances.html',
        {'grievances': grievances}
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
        return redirect('my_grievances')

    return render(
        request,
        'grievances/delete_grievance.html',
        {'grievance': grievance}
    )
