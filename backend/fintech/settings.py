"""
Django settings for fintech project.

This settings file is designed for:

- Django REST Framework
- JWT Authentication
- PostgreSQL
- Celery
- Redis
- Docker
- Custom User Model
"""

# ==========================================
# PYTHON IMPORTS
# ==========================================

# Access environment variables
import os

# Work with filesystem paths
from pathlib import Path

# Load .env file
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# PROJECT ROOT DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# SECURITY
# ==========================================

# Secret key used for:
# - sessions
# - JWT signing
# - password reset tokens
#
# Never commit real values to GitHub.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "unsafe-development-key"
)

# Turn OFF in production
DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"

# Allowed hosts
ALLOWED_HOSTS = [
    "*"
]


# ==========================================
# DJANGO APPS
# ==========================================

INSTALLED_APPS = [

    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps

    # Django REST Framework
    "rest_framework",

    # JWT Authentication
    "rest_framework_simplejwt",

    # Filtering support
    "django_filters",

    # Local apps
    "apps.accounts",
    "apps.wallets",
    "apps.transactions",
    "apps.audit",
]


# ==========================================
# MIDDLEWARE
# ==========================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================================
# URL CONFIGURATION
# ==========================================

ROOT_URLCONF = "fintech.urls"


# ==========================================
# TEMPLATES
# ==========================================

TEMPLATES = [
    {
        "BACKEND":
        "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==========================================
# WSGI
# ==========================================

WSGI_APPLICATION = "fintech.wsgi.application"


# ==========================================
# DATABASE
# ==========================================

DATABASES = {
    "default": {

        "ENGINE":
        "django.db.backends.postgresql",

        "NAME":
        os.getenv("DB_NAME"),

        "USER":
        os.getenv("DB_USER"),

        "PASSWORD":
        os.getenv("DB_PASSWORD"),

        "HOST":
        os.getenv("DB_HOST"),

        "PORT":
        os.getenv("DB_PORT"),
    }
}


# ==========================================
# CUSTOM USER MODEL
# ==========================================

AUTH_USER_MODEL = "accounts.User"


# ==========================================
# PASSWORD VALIDATION
# ==========================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==========================================
# INTERNATIONALIZATION
# ==========================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ==========================================
# STATIC FILES
# ==========================================

STATIC_URL = "static/"

STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)


# ==========================================
# MEDIA FILES
# ==========================================

MEDIA_URL = "/media/"

MEDIA_ROOT = (
    BASE_DIR / "media"
)


# ==========================================
# PRIMARY KEY TYPE
# ==========================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# ==========================================
# DJANGO REST FRAMEWORK
# ==========================================

REST_FRAMEWORK = {

    # JWT authentication
    "DEFAULT_AUTHENTICATION_CLASSES": (

        "rest_framework_simplejwt.authentication.JWTAuthentication",

    ),

    # Require authentication
    "DEFAULT_PERMISSION_CLASSES": (

        "rest_framework.permissions.IsAuthenticated",

    ),

    # Optional filtering
    "DEFAULT_FILTER_BACKENDS": (

        "django_filters.rest_framework.DjangoFilterBackend",

    ),
}


# ==========================================
# CELERY CONFIGURATION
# ==========================================

# Redis broker
CELERY_BROKER_URL = os.getenv(
    "REDIS_URL"
)

# Store task results in Redis
CELERY_RESULT_BACKEND = os.getenv(
    "REDIS_URL"
)

# UTC timezone
CELERY_ENABLE_UTC = True

# Message serialization
CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

# Accepted formats
CELERY_ACCEPT_CONTENT = [
    "json"
]


# ==========================================
# LOGGING
# ==========================================

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "handlers": {

        "console": {

            "class":
            "logging.StreamHandler",
        },
    },

    "root": {

        "handlers":
        ["console"],

        "level":
        "INFO",
    },
}


# ==========================================
# SECURITY SETTINGS
# ==========================================
#
# Enable in production later
#

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "DENY"