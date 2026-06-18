# services/payment_service.py

from base.models import Billing, Appointment
from doctor.models import Notification as DoctorNotification
from patient.models import Notification as PatientNotification
from base.signals import payment_completed 

class PaymentService:
    @staticmethod
    def mark_as_paid(billing: Billing):
        if billing.status != Billing.BILLING_STATUS_UNPAID:
            return

        billing.status = Billing.BILLING_STATUS_PAID
        billing.save()

        # create signal
        payment_completed.send_robust(sender=Billing, billing=billing)

        appointment = billing.appointment
        appointment.status = Appointment.APPOINTMENT_STATUS_SCHEDULED
        appointment.save()

