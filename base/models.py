from django.db import models
from django.shortcuts import reverse
from shortuuid.django_fields import ShortUUIDField

from collections import namedtuple

from patient.models import Patient
from doctor.models import Doctor

ImageData = namedtuple("ImageData", ["url", "alt"])

class Service(models.Model):
    image = models.ImageField(upload_to="images/services/",blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_doctors = models.ManyToManyField(Doctor, blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.cost}'

    def get_absolute_url(self):
        return reverse("service_datail", kwargs={"pk": self.pk})
    
    @property
    def image_data(self):
        if self.image:
            return ImageData(
                self.image.url,
                self.name or "Doctor"
            )

        return ImageData(
            "/media/images/doctors/default-service.jpg",
            "Default service image"
        )
    

class Appointment(models.Model):
    STATUS = [
        ('sch', 'Scheduled'), 
        ('com', 'Completed'), 
        ('pen', 'Pending'), 
        ('can', 'Cancelled')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_patient')
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=3, choices=STATUS)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.full_name} with {self.doctor.full_name}"
    

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.appointment.patient.full_name}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test_name}"


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField(blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.full_name}"
    

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True,  related_name='billings')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='billing', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=[('pa', 'Paid'), ('un', 'Unpaid')])
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Billing for {self.patient.full_name} - Total: {self.total}"
    