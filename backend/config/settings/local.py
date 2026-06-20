from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DJANGO_POSTGRES_DB", "hms"),
        "USER": env("DJANGO_POSTGRES_USER", "postgres"),
        "PASSWORD": env("DJANGO_POSTGRES_PASSWORD", "postgres"),
        "HOST": env("DJANGO_POSTGRES_HOST", "localhost"),
        "PORT": 5432,
    }
}