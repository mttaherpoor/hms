from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import UserType

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
