from .base import *

DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = [h for h in env("DJANGO_ALLOWED_HOSTS", "").split(",") if h]

SECRET_KEY = get_secret("django_secret_key")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DJANGO_POSTGRES_DB"),
        "USER": env("DJANGO_POSTGRES_USER"),
        "PASSWORD": get_secret("postgres_password"),
        "HOST": env("DJANGO_POSTGRES_HOST"),
        "PORT": 5432,
    }
}