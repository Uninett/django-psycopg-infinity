from django.db import models

from django_psycopg_infinity.fields import DateTimeInfinityField


class _NaiveDateTimeInfinityField(DateTimeInfinityField):
    """Force a `timestamp without time zone` column regardless of USE_TZ.

    Test-only field. The package's `DateTimeInfinityField` inherits Django's
    `DateTimeField.db_type()`, which selects `timestamptz` when USE_TZ is True.
    Overriding `db_type` here lets us exercise the `timestamp` (no tz) column
    path in the same test run without needing a second settings module.
    """

    def db_type(self, connection):
        return "timestamp"


class TestEvent(models.Model):
    name = models.CharField(max_length=100, default="test")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = DateTimeInfinityField(null=True, blank=True)

    class Meta:
        app_label = "tests"


class NaiveColumnEvent(models.Model):
    """Model backed by a `timestamp without time zone` column."""

    name = models.CharField(max_length=100, default="test")
    end_time = _NaiveDateTimeInfinityField(null=True, blank=True)

    class Meta:
        app_label = "tests"
