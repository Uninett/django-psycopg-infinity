import os

SECRET_KEY = "test-secret-key-not-for-production"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

USE_TZ = True

TIME_ZONE = "UTC"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "tests",
]

DATABASES = {
    "default": {
        "ENGINE": "django_pg_infinity.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "django_pg_infinity_test"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    },
}
