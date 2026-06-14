from django import forms

class AppointmentBookingForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    mobile = forms.CharField()
    gender = forms.CharField(required=False)
    address = forms.CharField(required=False)
    dob = forms.DateField(required=False)
    issues = forms.CharField()
    symptoms = forms.CharField()