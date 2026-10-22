from django import forms
from .models import Grievance


class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['title', 'category', 'student_class', 'is_hostel', 'room_number', 'description']
        labels = {
            'title': 'Title',
            'category': 'Category',
            'student_class': 'Class',
            'is_hostel': 'I am a hostel student',
            'room_number': 'Hostel Room No.',
            'description': 'Description',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter grievance title'
            }),
            'student_class': forms.TextInput(attrs={
                'placeholder': 'e.g. B.Tech CSE - 2nd Year'
            }),
            'room_number': forms.TextInput(attrs={
                'placeholder': 'e.g. B-204'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your grievance',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_class'].required = True
        self.fields['room_number'].required = False

    def clean(self):
        cleaned = super().clean()
        is_hostel = cleaned.get('is_hostel')
        room = (cleaned.get('room_number') or '').strip()