from django.db import models

class UserType(models.TextChoices):
    DOCTOR = "doc", "Doctor"
    PATIENT = "pat", "Patient"
    ADMIN = "adm", "Admin"