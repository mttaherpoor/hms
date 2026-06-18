from doctor.models import Notification as DoctorNotification
from patient.models import Notification as PatientNotification


class NotificationService:

    @staticmethod
    def create_booking_notifications(billing):

        appointment = billing.appointment

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
