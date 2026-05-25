from django.db import models
from django.utils import timezone
from django.conf import settings

BLOOD_GROOPS =(
    ('A+','A+'),('A-','A-'),
    ('B+','B+'),('B-','B-'),
    ('AB+','AB+'),('AB-','AB-'),
    ('O+','O+'),('O-','O-'),
)

NOTIFICATION_TYPE = (
    ("sch", "Appointment Scheduled"),
    ("can", "Appointment Cancelled"),
)


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/patients/", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(default=timezone.now, null=True, blank=True)
    blood_group = models.CharField(choices=BLOOD_GROOPS, max_length=3, null=True, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}"


class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True, related_name="patient_appointment_notification")
    type = models.CharField(max_length=3, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Notification"
    
    def __str__(self):
        return f"{self.patient.full_name} Notification"
