from datetime import datetime

from django.test import SimpleTestCase
from django.utils.timezone import is_aware

from django_psycopg_infinity.utils import (
    INFINITY,
    INFINITY_REPR,
    NEGATIVE_INFINITY,
    NEGATIVE_INFINITY_REPR,
    get_infinity_repr,
    get_infinity_time,
    make_aware,
    make_naive,
    parse_infinity,
)


class MakeAwareTests(SimpleTestCase):
    def test_naive_datetime_becomes_aware(self):
        naive = datetime(2020, 1, 1)
        result = make_aware(naive)
        self.assertTrue(is_aware(result))

    def test_aware_datetime_stays_aware(self):
        aware = make_aware(datetime(2020, 1, 1))
        result = make_aware(aware)
        self.assertTrue(is_aware(result))
        self.assertEqual(result, aware)


class MakeNaiveTests(SimpleTestCase):
    def test_aware_datetime_becomes_naive(self):
        aware = make_aware(datetime(2020, 1, 1))
        result = make_naive(aware)
        self.assertFalse(is_aware(result))

    def test_naive_datetime_stays_naive(self):
        naive = datetime(2020, 1, 1)
        result = make_naive(naive)
        self.assertFalse(is_aware(result))
        self.assertEqual(result, naive)


class GetInfinityReprTests(SimpleTestCase):
    def test_infinity_returns_string_repr(self):
        result = get_infinity_repr(INFINITY, str_repr=True)
        self.assertEqual(result, INFINITY_REPR)

    def test_negative_infinity_returns_string_repr(self):
        result = get_infinity_repr(NEGATIVE_INFINITY, str_repr=True)
        self.assertEqual(result, NEGATIVE_INFINITY_REPR)

    def test_infinity_returns_datetime_repr(self):
        result = get_infinity_repr(INFINITY, str_repr=False)
        self.assertEqual(result, INFINITY)

    def test_normal_datetime_returns_none(self):
        result = get_infinity_repr(datetime(2020, 1, 1), str_repr=True)
        self.assertIsNone(result)

    def test_non_datetime_returns_none(self):
        result = get_infinity_repr("not a datetime", str_repr=True)
        self.assertIsNone(result)


class GetInfinityTimeTests(SimpleTestCase):
    def test_infinity_datetime_returns_aware_infinity(self):
        result = get_infinity_time(INFINITY)
        self.assertIsNotNone(result)
        self.assertTrue(is_aware(result))
        self.assertEqual(result.replace(tzinfo=None), INFINITY)

    def test_infinity_string_returns_aware_infinity(self):
        result = get_infinity_time(INFINITY_REPR)
        self.assertIsNotNone(result)
        self.assertTrue(is_aware(result))
        self.assertEqual(result.replace(tzinfo=None), INFINITY)

    def test_normal_datetime_returns_none(self):
        result = get_infinity_time(datetime(2020, 1, 1))
        self.assertIsNone(result)

    def test_normal_string_returns_none(self):
        result = get_infinity_time("2020-01-01")
        self.assertIsNone(result)


class ParseInfinityTests(SimpleTestCase):
    def test_infinity_string_returns_localized(self):
        result = parse_infinity(INFINITY_REPR)
        self.assertIsNotNone(result)
        self.assertTrue(is_aware(result))

    def test_negative_infinity_string_returns_localized(self):
        result = parse_infinity(NEGATIVE_INFINITY_REPR)
        self.assertIsNotNone(result)
        self.assertTrue(is_aware(result))

    def test_infinity_string_returns_naive(self):
        result = parse_infinity(INFINITY_REPR, return_localized=False)
        self.assertEqual(result, INFINITY)
        self.assertFalse(is_aware(result))

    def test_normal_string_returns_none(self):
        result = parse_infinity("not infinity")
        self.assertIsNone(result)
