from .base import *

DEBUG = env.bool("DJANGO_DEBUG", False)

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

CSRF_TRUSTED_ORIGINS = [o for o in env("CSRF_TRUSTED_ORIGINS", "").split(",") if o]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = [h for h in env("DJANGO_ALLOWED_HOSTS", "").split(",") if h]
