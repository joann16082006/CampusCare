from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Profile
from .decorators import role_required


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@role_required('STUDENT', 'STAFF', 'ADMIN')
def dashboard_view(request):
    role = request.user.profile.role

    return render(request, 'accounts/dashboard.html', {
        'role': role,
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return redirect('dashboard')

@role_required('STUDENT')
def student_page(request):
    return render(request, 'accounts/student_page.html')


@role_required('STAFF')
def staff_page(request):
    return render(request, 'accounts/staff_page.html')

@role_required('STUDENT', 'STAFF', 'ADMIN')
def profile_view(request):
    return render(request, 'accounts/profile.html')