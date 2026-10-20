from django import forms
from .models import Grievance


class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['title', 'category', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter grievance title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your grievance',
                'rows': 5
            }),
        }