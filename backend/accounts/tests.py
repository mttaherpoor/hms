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
