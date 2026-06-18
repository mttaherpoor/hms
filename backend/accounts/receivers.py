from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, UserType
from doctor.models import Doctor
from patient.models import Patient

from base.signals import payment_completed
from accounts.services.email_service import EmailService
from accounts.services.notification_service import NotificationService


@receiver(payment_completed)
def handle_payment_completed(sender, billing, **kwargs):
    EmailService.send_booking_emails(billing)
    NotificationService.create_booking_notifications(billing)



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
