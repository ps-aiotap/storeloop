import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)  # Force .env to override system variables



# Simple logging control
# Add ENABLE_FILE_LOGGING=True to .env file to enable file logging
# Default: Console logging only

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key-for-development")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "tailwind",
    "theme",
    # Local apps
    "products",
    "orders",
    "stores",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "stores.middleware.StoreMiddleware",
    "stores.views.ClearMessagesMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "stores.context_processors.store_theme",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database - FORCED POSTGRESQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "storeloop"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# DEBUG: Print database configuration
print(f"DEBUG DATABASE CONFIG:")
print(f"  ENGINE: {DATABASES['default']['ENGINE']}")
print(f"  NAME: {DATABASES['default']['NAME']}")
print(f"  HOST: {DATABASES['default']['HOST']}")
print(f"  PORT: {DATABASES['default']['PORT']}")
print(f"  USER: {DATABASES['default']['USER']}")
print(f"  ENV DB_PORT: {os.environ.get('DB_PORT', 'NOT SET')}")
print(f"  ENV DB_HOST: {os.environ.get('DB_HOST', 'NOT SET')}")
print(f"  ENV DB_NAME: {os.environ.get('DB_NAME', 'NOT SET')}")
print(f"  ENV DB_USER: {os.environ.get('DB_USER', 'NOT SET')}")
print(f"  ENV USE_SQLITE: {os.environ.get('USE_SQLITE', 'NOT SET')}")
print("=" * 50)

# Auto-create PostgreSQL database if it doesn't exist
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database_if_not_exists():
    try:
        # Try to connect to the target database
        conn = psycopg2.connect(
            host=DATABASES["default"]["HOST"],
            port=DATABASES["default"]["PORT"],
            user=DATABASES["default"]["USER"],
            password=DATABASES["default"]["PASSWORD"],
            database=DATABASES["default"]["NAME"],
        )
        conn.close()
    except psycopg2.OperationalError as e:
        if "does not exist" in str(e):
            # Database doesn't exist, create it
            conn = psycopg2.connect(
                host=DATABASES["default"]["HOST"],
                port=DATABASES["default"]["PORT"],
                user=DATABASES["default"]["USER"],
                password=DATABASES["default"]["PASSWORD"],
                database="postgres",  # Connect to default postgres database
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {DATABASES['default']['NAME']}")
            cursor.close()
            conn.close()
            print(f"Created database: {DATABASES['default']['NAME']}")


# Only create database during migrations or runserver
import sys

if "migrate" in sys.argv or "runserver" in sys.argv:
    try:
        create_database_if_not_exists()
    except Exception as e:
        print(f"Warning: Could not auto-create database: {e}")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Language support
LANGUAGES = [
    ("en", "English"),
    ("hi", "हिंदी"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Database encoding for Unicode support
DATABASE_OPTIONS = {
    "charset": "utf8mb4",
    "use_unicode": True,
}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "staticcss"),
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Tailwind configuration
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = [
    "127.0.0.1",
]

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@storeloop.com"

# Razorpay settings
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")
RAZORPAY_TEST_MODE = True

# Login redirect
LOGIN_REDIRECT_URL = "/stores/"
LOGIN_URL = "/accounts/login/"

# Additional settings for Indian locale
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

# Ensure proper Unicode handling
DEFAULT_CHARSET = "utf-8"

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True

# Simple logging toggle via environment variable
# Set ENABLE_FILE_LOGGING=True in .env to enable file logging
if os.environ.get("ENABLE_FILE_LOGGING", "False").lower() == "true":
    # Create logs directory
    LOGS_DIR = BASE_DIR / "logs"
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": LOGS_DIR / "django.log",
            },
        },
        "root": {
            "handlers": ["file"],
            "level": "ERROR",
        },
    }
else:
    # Console logging only (default)
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
