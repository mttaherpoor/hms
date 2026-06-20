from pathlib import Path
from environs import Env
from django.contrib.messages import constants as messages

from config import jazzmin

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = Env()
env.read_env()


def get_secret(secret_name, default=None):
    secret_file = Path(f"/run/secrets/{secret_name}")

    if secret_file.exists():
        return secret_file.read_text().strip()

    return default


# ---------------- CORE ----------------

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "import_export",
    "crispy_forms",
    "crispy_bootstrap5",
    "anymail",

    'base',
    'accounts',
    'doctor',
    'patient',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "base.context_processors.services",
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ---------------- AUTH ----------------

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# ---------------- I18N ----------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True


# ---------------- STATIC / MEDIA ----------------

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------- JAZZMIN ----------------

JAZZMIN_SETTINGS = jazzmin.JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = jazzmin.JAZZMIN_UI_TWEAKS


# ---------------- MESSAGES ----------------

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


# ---------------- EMAIL ----------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = get_secret("email_password")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
FROM_EMAIL = EMAIL_HOST_USER


# ---------------- THIRD PARTY ----------------

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# ---------------- PAYMENTS ----------------

STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY", default="")
STRIPE_SECRET_KEY = get_secret("stripe_secret_key")

PAYPAL_CLIENT_ID = env("PAYPAL_CLIENT_ID", default="")
PAYPAL_SECRET_ID = get_secret("paypal_secret")