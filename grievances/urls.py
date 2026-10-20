from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_grievance, name='submit_grievance'),
    path('my-grievances/', views.my_grievances, name='my_grievances'),
]