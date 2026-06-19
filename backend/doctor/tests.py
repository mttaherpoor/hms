from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import UserType
from doctor.models import Doctor, Notification
from patient.models import Patient
from base.models import Service, Appointment, Billing

User = get_user_model()


class DoctorBaseMixin:

    @classmethod
    def create_doctor(cls):
        user = User.objects.create_user(
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )
        return Doctor.objects.get(user=user)

    @classmethod
    def create_patient(cls):
        user = User.objects.create_user(
            email="patient@test.com",
            password="pass123",
            user_type=UserType.PATIENT,
        )
        return Patient.objects.get(user=user)

    @classmethod
    def create_service(cls):
        return Service.objects.create(
            name="Dermatology",
            cost=100,
        )
    

class DoctorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )

        cls.doctor = Doctor.objects.get(user=user)
        cls.doctor.full_name = "John Doe"
        cls.doctor.save()

    def test_str_representation(self):
        self.assertEqual(str(self.doctor), "Dr. John Doe")

    def test_default_image(self):
        self.assertIn(
            "default-doctor",
            self.doctor.image_data.url,
        )


class DashboardViewTest(DoctorBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.doctor = cls.create_doctor()

    def test_login_required(self):
        response = self.client.get(
            reverse("doctor:dashboard")
        )

        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads(self):
        self.client.force_login(self.doctor.user)

        response = self.client.get(
            reverse("doctor:dashboard")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.view_name,
            "doctor:dashboard"
        )


class AppointmentCancelViewTest(DoctorBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.doctor = cls.create_doctor()
        cls.patient = cls.create_patient()
        cls.service = cls.create_service()

        cls.appointment = Appointment.objects.create(
            doctor=cls.doctor,
            patient=cls.patient,
            service=cls.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING,
        )

    def test_cancel_appointment(self):

        self.client.force_login(self.doctor.user)

        response = self.client.post(
            reverse(
                "doctor:appointment-cancel",
                kwargs={
                    "appointment_id":
                    self.appointment.appointment_id
                }
            )
        )

        self.assertEqual(response.status_code, 302)

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.APPOINTMENT_STATUS_CANCELLED,
        )


class AppointmentActivateViewTest(DoctorBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.doctor = cls.create_doctor()
        cls.patient = cls.create_patient()
        cls.service = cls.create_service()

        cls.appointment = Appointment.objects.create(
            doctor=cls.doctor,
            patient=cls.patient,
            service=cls.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING,
        )

    def test_activate_appointment(self):

        self.client.force_login(self.doctor.user)

        self.client.post(
            reverse(
                "doctor:appointment-activate",
                kwargs={
                    "appointment_id":
                    self.appointment.appointment_id
                }
            )
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.APPOINTMENT_STATUS_SCHEDULED,
        )


class AppointmentCompletedViewTest(DoctorBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.doctor = cls.create_doctor()
        cls.patient = cls.create_patient()
        cls.service = cls.create_service()

        cls.appointment = Appointment.objects.create(
            doctor=cls.doctor,
            patient=cls.patient,
            service=cls.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING,
        )

    def test_complete_appointment(self):

        self.client.force_login(self.doctor.user)

        self.client.post(
            reverse(
                "doctor:appointment-completed",
                kwargs={
                    "appointment_id":
                    self.appointment.appointment_id
                }
            )
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            Appointment.APPOINTMENT_STATUS_COMPLETED,
        )


class PaymentViewTest(DoctorBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.doctor = cls.create_doctor()
        cls.patient = cls.create_patient()
        cls.service = cls.create_service()

        cls.appointment = Appointment.objects.create(
            doctor=cls.doctor,
            patient=cls.patient,
            service=cls.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING,
        )

        Billing.objects.create(
            appointment=cls.appointment,
            patient=cls.patient,
            sub_total=100,
            tax=5,
            total=105,
            status=Billing.BILLING_STATUS_PAID,
        )

    def test_payment_page_loads(self):

        self.client.force_login(self.doctor.user)

        response = self.client.get(
            reverse("doctor:payments")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["payments"]),
            1,
        )


class NotificationSeenViewTest(DoctorBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.doctor = cls.create_doctor()
        cls.service = cls.create_service()
        cls.patient = cls.create_patient()

        cls.appointment = Appointment.objects.create(
            doctor=cls.doctor,
            patient=cls.patient,
            service=cls.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING,
        )

        cls.notification = Notification.objects.create(
            doctor=cls.doctor,
            appointment=cls.appointment,
            type=Notification.NEW_APPOINTMENT,
        )

    def test_mark_notification_seen(self):

        self.client.force_login(self.doctor.user)

        self.client.post(
            reverse(
                "doctor:notification-seen",
                kwargs={
                    "pk": self.notification.pk
                }
            )
        )

        self.notification.refresh_from_db()

        self.assertTrue(self.notification.seen)


class ProfileViewTest(DoctorBaseMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.doctor = cls.create_doctor()

    def test_profile_update(self):

        self.client.force_login(self.doctor.user)

        response = self.client.post(
            reverse("doctor:profile"),
            {
                "full_name": "John Doe",
                "country": "Germany",
                "mobile": "123456",
                "bio": "Doctor",
                "specialization": "Cardiology",
                "qualifications": "MD",
                "years_of_experience": "10",
                "next_available_appointment_date": "2030-01-01",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.doctor.refresh_from_db()

        self.assertEqual(
            self.doctor.full_name,
            "John Doe",
        )
