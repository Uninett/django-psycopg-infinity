from datetime import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime


INFINITY_REPR = "infinity"
NEGATIVE_INFINITY_REPR = f"-{INFINITY_REPR}"

INFINITY = datetime.max
NEGATIVE_INFINITY = datetime.min


def _get_local_timezone():
    return timezone.get_default_timezone()


def make_aware(value: datetime):
    if timezone.is_aware(value):
        return value
    # .replace() instead of timezone.make_aware() to avoid OverflowError on datetime.max/min
    return value.replace(tzinfo=_get_local_timezone())


def make_naive(value: datetime):
    if timezone.is_naive(value):
        return value
    # .replace() instead of timezone.make_naive() to avoid OverflowError on datetime.max/min
    return value.replace(tzinfo=None)


def get_infinity_repr(value, *, str_repr):
    if not isinstance(value, datetime):
        return None

    naive = value.replace(tzinfo=None) if value.tzinfo else value
    if naive == INFINITY:
        return INFINITY_REPR if str_repr else INFINITY
    elif naive == NEGATIVE_INFINITY:
        return NEGATIVE_INFINITY_REPR if str_repr else NEGATIVE_INFINITY
    return None


def get_infinity_time(value):
    if isinstance(value, datetime):
        naive = value.replace(tzinfo=None) if value.tzinfo else value
        if naive == INFINITY or naive == NEGATIVE_INFINITY:
            return make_aware(naive)
    elif isinstance(value, str):
        return parse_infinity(value)
    return None


def parse_infinity(value: str, *, return_localized=True):
    if value == INFINITY_REPR:
        return make_aware(INFINITY) if return_localized else INFINITY
    elif value == NEGATIVE_INFINITY_REPR:
        return make_aware(NEGATIVE_INFINITY) if return_localized else NEGATIVE_INFINITY
    return None


# Based on django/db/backends/sqlite3/operations.py (Django 5.2)
def convert_datetimefield_value(value, connection):
    if value is not None:
        if not isinstance(value, datetime):
            value = parse_datetime(value)
        if settings.USE_TZ and not timezone.is_aware(value):
            value = timezone.make_aware(value, connection.timezone)
    return value
