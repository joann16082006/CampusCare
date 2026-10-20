from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']