# services/payment_service.py

from base.models import Billing, Appointment
from doctor.models import Notification as DoctorNotification
from patient.models import Notification as PatientNotification


class PaymentService:
    @staticmethod
    def mark_as_paid(billing: Billing):
        if billing.status != Billing.BILLING_STATUS_UNPAID:
            return

        billing.status = Billing.BILLING_STATUS_PAID
        billing.save()

        appointment = billing.appointment
        appointment.status = Appointment.APPOINTMENT_STATUS_SCHEDULED
        appointment.save()

        DoctorNotification.objects.create(
            doctor=appointment.doctor,
            appointment=appointment,
            type=DoctorNotification.NEW_APPOINTMENT
        )

        PatientNotification.objects.create(
            patient=appointment.patient,
            appointment=appointment,
            type=PatientNotification.APPOINTMENT_SCHEDULED
        )
