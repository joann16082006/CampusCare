from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('student-page/', views.student_page, name='student_page'),
    path('staff-page/', views.staff_page, name='staff_page'),
    path('profile/', views.profile_view, name='profile'),
]