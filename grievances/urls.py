from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_grievance, name='submit_grievance'),
    path('my-grievances/', views.my_grievances, name='my_grievances'),
    path('staff/', views.staff_grievances, name='staff_grievances'),
    path(
        '<int:grievance_id>/update-status/',
        views.update_grievance_status,
        name='update_grievance_status',
    ),
    path(
        '<int:grievance_id>/history/',
        views.grievance_history,
        name='grievance_history',
    ),
]