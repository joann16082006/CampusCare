from django.shortcuts import render, redirect
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