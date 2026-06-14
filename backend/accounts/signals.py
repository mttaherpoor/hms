from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, UserType
from doctor.models import Doctor
from patient.models import Patient

PROFILE_MODELS = {
    UserType.DOCTOR: Doctor,
    UserType.PATIENT: Patient,
}

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance:CustomUser, created, **kwargs):
    if not created:
        return

    profile_model = PROFILE_MODELS.get(instance.user_type)

    if profile_model:
        profile_model.objects.create(user=instance)