# forms.py

from django import forms

from .models import Doctor

class DoctorForm(forms.ModelForm):
    next_available_appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    
    class Meta:
        model = Doctor
        fields = (
            "full_name",
            "image",
            "country",
            "mobile",
            "bio",
            "specialization",
            "qualifications",
            "years_of_experience",
            "next_available_appointment_date",           
        )
