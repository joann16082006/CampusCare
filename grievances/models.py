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

class GrievanceHistory(models.Model):
    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name='history'
    )

    staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grievance_history'
    )

    previous_status = models.CharField(
        max_length=20,
        choices=Grievance.STATUS_CHOICES
    )

    new_status = models.CharField(
        max_length=20,
        choices=Grievance.STATUS_CHOICES
    )

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.grievance.title}: '
            f'{self.previous_status} → {self.new_status}'
        )