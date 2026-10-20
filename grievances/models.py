from django.db import models
from django.contrib.auth.models import User


class Grievance(models.Model):
    CATEGORY_CHOICES = [
        ('ACADEMIC', 'Academic'),
        ('FACILITY', 'Facility'),
        ('HOSTEL', 'Hostel'),
        ('TRANSPORT', 'Transport'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='grievances'
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title