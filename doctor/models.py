from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.utils import timezone

from collections import namedtuple

ImageData = namedtuple("ImageData", ["url", "alt"])

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/doctors/", blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    
    country = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=100, blank=True)

    specialization = models.CharField(max_length=100, blank=True)
    qualifications = models.CharField(max_length=100, blank=True)
    
    years_of_experience = models.CharField(max_length=100, blank=True)
    next_available_appointment_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    DEFAULT_IMAGE = "images/defaults/default-doctor.jpg"
    
    def __str__(self):
        return f"Dr. {self.full_name}"

    @property
    def image_data(self):
        if self.image:
            return ImageData(
                self.image.url,
                self.full_name or "Doctor"
            )

        return ImageData(
            static(self.DEFAULT_IMAGE),
            "Default doctor image"
        )
    

NOTIFICATION_TYPE = (
    ("new", "New Appointment"),
    ("can", "Appointment Cancelled"),
)


class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True)
    appointment = models.ForeignKey('base.Appointment', on_delete=models.CASCADE, blank=True,
                                     related_name="doctor_appointment_notification")
    type = models.CharField(max_length=3, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Notification"
    
    def __str__(self):
        return f"Dr {self.doctor.full_name} Notification"
    