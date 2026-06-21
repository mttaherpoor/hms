from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .constants import UserType


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,max_length=50)
    username = models.CharField(max_length=50, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    user_type = models.CharField(max_length=3, choices=UserType.choices, default=UserType.PATIENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']

    objects=CustomUserManager()

    def __str__(self:AbstractUser) -> str:
        return self.username
    
    def save(self:AbstractUser, *args, **kwargs):
        email_username, _ = self.email.split('@')

        self.username = email_username if (self.username=='' or self.username==None) else self.username

        super(CustomUser,self).save(*args, **kwargs)
