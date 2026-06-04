# forms.py

from django import forms

from .models import Patient

class PatientForm(forms.ModelForm):
    issues = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
        }),
        required=False,
    )

    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
        }),
        required=False,
    )

    class Meta:
        model = Patient
        fields = (
            "full_name",
            "mobile",
            "gender",
            "address",
            "dob",
            "blood_group",
        )

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "John Doe",
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+123 (456) 7890",
            }),
            "gender": forms.Select(attrs={
                "class": "form-select",
            }),
            "dob": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "123 Main Street",
            }),
            "blood_group": forms.Select(attrs={
                "class": "form-select",
            }),
        }
