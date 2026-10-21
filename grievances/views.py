
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

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

    # Show 5 grievances per page
    page_obj = Paginator(grievances, 5).get_page(
        request.GET.get('page')
    )

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
