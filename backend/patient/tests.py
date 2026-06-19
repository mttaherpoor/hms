from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from accounts.models import UserType
from doctor.models import Doctor
from patient.models import Patient
from base.models import Service, Appointment, Billing

User = get_user_model()


class PatientBaseMixin:

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        doctor_user = User.objects.create_user(
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )
        cls.doctor = Doctor.objects.get(user=doctor_user)

        patient_user = User.objects.create_user(
            email="patient@test.com",
            password="pass123",
            user_type=UserType.PATIENT,
        )
        cls.patient = Patient.objects.get(user=patient_user)

        cls.service = Service.objects.create(
            name="Dermatology",
            cost=100,
        )

    @classmethod
    def create_appointment(
        cls,
        status=Appointment.APPOINTMENT_STATUS_PENDING,
    ):
        return Appointment.objects.create(
            doctor=cls.doctor,
            patient=cls.patient,
            service=cls.service,
            status=status,
        )

    @classmethod
    def create_billing(
        cls,
        status=Billing.BILLING_STATUS_PAID,
    ):
        appointment = cls.create_appointment()

        return Billing.objects.create(
            appointment=appointment,
            patient=cls.patient,
            sub_total=100,
            tax=5,
            total=105,
            status=status,
        )


class PatientModelTest(PatientBaseMixin,TestCase):

    def test_str_representation(self):
        self.patient.full_name = "John Doe"
        self.patient.save()

        self.assertEqual(
            str(self.patient),
            "John Doe",
        )

    def test_default_image(self):
        self.assertIn(
            "default-patient",
            self.patient.image_data.url,
        )


class DashboardViewTest(PatientBaseMixin, TestCase):

    def test_login_required(self):
        response = self.client.get(
            reverse("patient:dashboard")
        )

        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads(self):
        self.client.force_login(self.patient.user)

        response = self.client.get(
            reverse("patient:dashboard")
        )

        self.assertEqual(response.status_code, 200)


class AppointmentCancelViewTest(PatientBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.appointment = cls.create_appointment()

    def test_cancel_appointment(self):
        self.client.force_login(self.patient.user)

        self.client.post(
            reverse(
                "patient:appointment-cancel",
                kwargs={
                    "appointment_id":
                    self.appointment.appointment_id
                },
            )
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.APPOINTMENT_STATUS_CANCELLED,
        )


class AppointmentActivateViewTest(PatientBaseMixin,TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.appointment = cls.create_appointment(
            Appointment.APPOINTMENT_STATUS_CANCELLED
        )

    def test_activate_appointment(self):
        self.client.force_login(self.patient.user)

        self.client.post(
            reverse(
                "patient:appointment-activate",
                kwargs={
                    "appointment_id":
                    self.appointment.appointment_id
                },
            )
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.APPOINTMENT_STATUS_SCHEDULED,
        )


class AppointmentCompletedViewTest(PatientBaseMixin,TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.appointment = cls.create_appointment(
            Appointment.APPOINTMENT_STATUS_SCHEDULED
        )

    def test_complete_appointment(self):
        self.client.force_login(self.patient.user)

        self.client.post(
            reverse(
                "patient:appointment-completed",
                kwargs={
                    "appointment_id":
                    self.appointment.appointment_id
                },
            )
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.APPOINTMENT_STATUS_COMPLETED,
        )


class AppointmentCompletedViewTest(PatientBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.appointment = cls.create_appointment(
            Appointment.APPOINTMENT_STATUS_SCHEDULED
        )

    def test_complete_appointment(self):
        self.client.force_login(self.patient.user)

        self.client.post(
            reverse(
                "patient:appointment-completed",
                kwargs={
                    "appointment_id":
                    self.appointment.appointment_id
                },
            )
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.APPOINTMENT_STATUS_COMPLETED,
        )


class PaymentViewTest(PatientBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.billing = cls.create_billing()

    def test_payment_page_loads(self):
        self.client.force_login(self.patient.user)

        response = self.client.get(
            reverse("patient:payments")
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.context["payments"]),
            1,
        )

class NotificationSeenViewTest(PatientBaseMixin,TestCase):
    @classmethod
    def create_notification(cls):
        from patient.models import Notification

        appointment = cls.create_appointment()

        return Notification.objects.create(
            patient=cls.patient,
            appointment=appointment,
            type=Notification.APPOINTMENT_SCHEDULED,
        )
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.notification = cls.create_notification()

    def test_mark_notification_seen(self):
        self.client.force_login(self.patient.user)

        self.client.post(
            reverse(
                "patient:notification-seen",
                kwargs={
                    "pk": self.notification.pk
                },
            )
        )

        self.notification.refresh_from_db()

        self.assertTrue(
            self.notification.seen
        )


class ProfileViewTest(PatientBaseMixin, TestCase):

    def test_profile_update(self):
        self.client.force_login(self.patient.user)

        response = self.client.post(
            reverse("patient:profile"),
            {
                "full_name": "John Doe",
                "mobile": "123456",
                "gender": Patient.GENDER_MALE,
                "address": "Germany",
                "dob": "2000-01-01",
                "blood_group": "A+",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.patient.refresh_from_db()

        self.assertEqual(
            self.patient.full_name,
            "John Doe",
        )
