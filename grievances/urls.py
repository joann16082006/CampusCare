
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_grievance, name='submit_grievance'),
    path('my-grievances/', views.my_grievances, name='my_grievances'),

    path(
        'edit/<int:pk>/',
        views.edit_grievance,
        name='edit_grievance'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_grievance,
        name='delete_grievance'
    ),
]
