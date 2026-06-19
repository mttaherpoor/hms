from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from accounts.models import UserType
from patient.models import Patient
from doctor.models import Doctor

User = get_user_model()

class UserModelTest(TestCase):

    def test_username_generated_from_email(self):
        user = User.objects.create_user(
            username="",
            email="john@example.com",
            password="pass123",
            user_type=UserType.PATIENT,
        )

        self.assertEqual(user.username, "john")


class ProfileCreationSignalTest(TestCase):

    def test_patient_profile_created(self):
        user = User.objects.create_user(
            username="",
            email="patient@test.com",
            password="pass123",
            user_type=UserType.PATIENT,
        )

        self.assertTrue(Patient.objects.filter(user=user).exists())

    def test_doctor_profile_created(self):
        user = User.objects.create_user(
            username="",
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )

        self.assertTrue(Doctor.objects.filter(user=user).exists())


class PaymentCompletedSignalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.patient_user = User.objects.create_user(
            email="patient@test.com",
            password="pass123",
            user_type=UserType.PATIENT,
        )
        cls.patient = Patient.objects.get(user=cls.patient_user)

        cls.doctor_user = User.objects.create_user(
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )
        cls.doctor = Doctor.objects.get(user=cls.doctor_user)

        from base.models import Service

        cls.service = Service.objects.create(
            name="General Checkup",
            cost=100,
        )
        cls.service.available_doctors.set([cls.doctor])

    @patch("accounts.services.email_service.EmailService.send_booking_emails")
    @patch("accounts.services.notification_service.NotificationService.create_booking_notifications")
    def test_payment_completed_signal(self, mock_notification, mock_email):

        from base.signals import payment_completed
        from base.models import Appointment, Billing

        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            service=self.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING
        )

        billing = Billing.objects.create(
            appointment=appointment,
            patient=self.patient,
            sub_total=100,
            tax=5,
            total= 105,
            status=Billing.BILLING_STATUS_PAID,
        )


        payment_completed.send(sender=self.__class__,billing=billing)

        mock_email.assert_called_once_with(billing)

        mock_notification.assert_called_once_with(billing)
