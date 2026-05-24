from django.db import models
from django.utils import timezone
from django.conf import settings

BLOOD_GROOPS =(
    ('A+','A+'),('A-','A-'),
    ('B+','B+'),('B-','B-'),
    ('AB+','AB+'),('AB-','AB-'),
    ('O+','O+'),('O-','O-'),
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

    def __str__(self):
        return f"{self.full_name}"
