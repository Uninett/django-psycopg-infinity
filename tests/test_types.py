from unittest import TestCase

from datetime import datetime, timedelta

from django_psycopg_infinity.types import Infinity, MinusInfinity


class TestCommonDunders(TestCase):
    def test_infinities_are_truthy(self):
        self.assertTrue(Infinity)
        self.assertTrue(MinusInfinity)


class TestInfinity(TestCase):
    def test_str_of_infinity_is_defined(self):
        self.assertEqual(str(Infinity), "infinity")

    def test_when_comparing_with_datetime_then_infinity_is_always_largest(self):
        self.assertTrue(Infinity > datetime.now())
        self.assertTrue(Infinity > MinusInfinity)
        self.assertTrue(datetime.now() < Infinity)
        self.assertTrue(MinusInfinity < Infinity)

    def test_when_comparing_with_self_then_equal(self):
        self.assertEqual(Infinity, Infinity)

    def test_when_comparing_with_datetime_then_not_equal(self):
        self.assertNotEqual(Infinity, datetime.now())
        self.assertNotEqual(Infinity, MinusInfinity)
        self.assertNotEqual(datetime.now(), Infinity)
        self.assertNotEqual(MinusInfinity, Infinity)

    def test_when_adding_a_timedelta_then_the_result_is_no_change(self):
        result = Infinity + timedelta(days=100000)
        self.assertEqual(result, Infinity)

    def test_when_subtracting_a_timedelta_then_the_result_is_no_change(self):
        result = Infinity - timedelta(days=100000)
        self.assertEqual(result, Infinity)

    def test_when_adding_a_datetime_then_the_result_is_no_change(self):
        result = Infinity + datetime.now()
        self.assertEqual(result, timedelta(0))
        result = Infinity + Infinity
        self.assertEqual(result, timedelta(0))


class TestMinusInfinity(TestCase):
    def test_str_of_infinity_is_defined(self):
        self.assertEqual(str(MinusInfinity), "-infinity")

    def test_when_comparing_with_datetime_then_minus_infinity_is_always_smallest(self):
        self.assertTrue(MinusInfinity < datetime.now())
        self.assertTrue(MinusInfinity < Infinity)
        self.assertTrue(datetime.now() > MinusInfinity)
        self.assertTrue(Infinity > MinusInfinity)

    def test_when_comparing_with_self_then_equal(self):
        self.assertTrue(MinusInfinity == MinusInfinity)

    def test_when_comparing_with_datetime_then_not_equal(self):
        self.assertNotEqual(MinusInfinity, datetime.now())
        self.assertNotEqual(MinusInfinity, Infinity)
        self.assertNotEqual(datetime.now(), MinusInfinity)
        self.assertNotEqual(Infinity, MinusInfinity)

    def test_when_adding_a_datetime_then_the_result_is_no_change(self):
        result = Infinity + Infinity
        self.assertEqual(result, Infinity)

    def test_when_adding_a_timedelta_then_the_result_is_no_change(self):
        result = MinusInfinity + timedelta(days=100000)
        self.assertEqual(result, MinusInfinity)

    def test_when_subtracting_a_timedelta_then_the_result_is_no_change(self):
        result = MinusInfinity - timedelta(days=100000)
        self.assertEqual(result, MinusInfinity)

    def test_when_adding_a_datetime_then_the_result_is_no_change(self):
        result = MinusInfinity + datetime.now()
        self.assertEqual(result, timedelta(0))
        result = MinusInfinity + MinusInfinity
        self.assertEqual(result, timedelta(0))
