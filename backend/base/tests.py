from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from decimal import Decimal

from accounts.models import UserType
from base.models import Service, Appointment, Billing
from patient.models import Patient
from doctor.models import Doctor

User = get_user_model()


class ServiceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            name="Cardiology",
            cost=Decimal("100.00"),
        )

    def test_str_representation(self):
        self.assertEqual(str(self.service), "Cardiology - 100.00")

    def test_image_data_returns_default_image(self):
        self.assertIn("default", self.service.image_data.url.lower())


class HomePageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            name="Cardiology",
            cost=Decimal("100.00"),
        )

    def test_home_page_url_resolves(self):
        url = reverse("base:home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.view_name, "base:home")

    def test_home_page_lists_services(self):
        url = reverse("base:home")
        response = self.client.get(url)

        self.assertIn("services", response.context)
        self.assertEqual(len(response.context["services"]), 1)


class ServiceDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            name="Cardiology",
            cost=Decimal("100.00"),
        )

    def test_service_detail_success(self):
        url = reverse("base:service-detail", kwargs={"pk": self.service.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.view_name, "base:service-detail")

    def test_service_detail_404(self):
        url = reverse("base:service-detail", kwargs={"pk": 99999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class BookAppointmentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            name="Dermatology",
            cost=Decimal("100.00"),
        )

        cls.user = User.objects.create_user(
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )
        cls.doctor = Doctor.objects.get(user=cls.user)

        patient_user = User.objects.create_user(
            email="patient@test.com",
            password="pass123",
            user_type=UserType.PATIENT,
        )

        cls.patient = Patient.objects.get(user=patient_user)


    def test_redirect_if_not_authenticated(self):
        url = reverse(
            "base:book-appointment",
            kwargs={
                "service_id": self.service.pk,
                "doctor_id": self.doctor.pk,
            },
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_booking_creates_appointment_and_billing_correctly(self):

        url = reverse(
            "base:book-appointment",
            kwargs={
                "service_id": self.service.pk,
                "doctor_id": self.doctor.pk,
            },
        )

        self.client.force_login(self.patient.user)

        response = self.client.post(url, {
            "full_name": "John Doe",
            "mobile": "123456",
            "gender": "mal",
            "dob": "2000-01-01",
            "address": "test",
            "issues": "headache",
            "symptoms": "fever",
        })
        self.assertEqual(response.status_code, 302)

        # ===== Appointment check =====
        appointment = Appointment.objects.first()
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.service, self.service)
        self.assertEqual(appointment.doctor, self.doctor)
        self.assertEqual(appointment.patient, self.patient)

        # ===== Billing check =====
        billing = Billing.objects.first()
        self.assertIsNotNone(billing)

        self.assertEqual(billing.sub_total, self.service.cost)

        # TAX = 5%
        expected_tax = (self.service.cost * Decimal("0.05"))
        expected_total = (self.service.cost + expected_tax)

        self.assertEqual(billing.tax, expected_tax)
        self.assertEqual(billing.total, expected_total)    


class CheckoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            name="Dermatology",
            cost=Decimal("100.00"),
        )

        cls.user = User.objects.create_user(
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )
        cls.doctor = Doctor.objects.get(user=cls.user)

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

        cls.appointment = Appointment.objects.create(
            patient=cls.patient,
            doctor=cls.doctor,
            service=cls.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING
        )
        cls.billing = Billing.objects.create(
            appointment=cls.appointment,
            patient=cls.patient,
            sub_total=100,
            tax=5,
            total=105,
            status=Billing.BILLING_STATUS_UNPAID,
        )

    def test_checkout_requires_login(self):
        response = self.client.get(
            reverse(
                "base:checkout",
                kwargs={
                    "billing_id": self.billing.billing_id
                },
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_checkout_page_loads(self):
        self.client.force_login(self.patient.user)

        response = self.client.get(
            reverse(
                "base:checkout",
                kwargs={
                    "billing_id": self.billing.billing_id
                },
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("stripe_public_key", response.context)

        self.assertIn("paypal_client_id", response.context)


class PaymentStatusViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        patient_user = User.objects.create_user(
            email="patient@test.com",
            password="pass123",
            user_type=UserType.PATIENT,
        )
        cls.patient = Patient.objects.get(user=patient_user)

        cls.user = User.objects.create_user(
            email="doctor@test.com",
            password="pass123",
            user_type=UserType.DOCTOR,
        )

        cls.doctor = Doctor.objects.get(user=cls.user)

        cls.service = Service.objects.create(
            name="Dermatology",
            cost=100,
        )

        cls.appointment = Appointment.objects.create(
            patient=cls.patient,
            doctor=cls.doctor,
            service=cls.service,
            status=Appointment.APPOINTMENT_STATUS_PENDING
        )
        cls.billing = Billing.objects.create(
            appointment=cls.appointment,
            patient=cls.patient,
            sub_total=100,
            tax=5,
            total=105,
            status=Billing.BILLING_STATUS_UNPAID,
        )

    def test_payment_status_view_success(self):
        self.client.force_login(self.patient.user)

        url = reverse("base:payment-status", kwargs={
            "billing_id": self.billing.billing_id
        }) + "?payment_status=success"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["payment_status"], "success")

        self.assertEqual(response.resolver_match.view_name, "base:payment-status")
