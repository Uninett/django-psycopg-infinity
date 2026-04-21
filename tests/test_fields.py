from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import is_aware, make_aware

from tests.models import TestEvent


class DateTimeInfinityFieldTests(TestCase):
    def setUp(self):
        self.event1 = TestEvent.objects.create(name="event1")
        self.event2 = TestEvent.objects.create(name="event2")
        self.event3 = TestEvent.objects.create(name="event3")

    @staticmethod
    def _save_end_time(event, end_time):
        event.end_time = end_time
        event.save(update_fields=["end_time"])

    def _assert_inserting_infinity_end_time_retrieves(self, insert_value, retrieval_value):
        self._save_end_time(self.event1, insert_value)
        self.event1.refresh_from_db()
        self.assertTrue(is_aware(self.event1.end_time))
        self.assertEqual(self.event1.end_time.replace(tzinfo=None), retrieval_value)

    def test_inserting_infinity_values_retrieves_infinity_values(self):
        self._assert_inserting_infinity_end_time_retrieves(datetime.max, datetime.max)
        self._assert_inserting_infinity_end_time_retrieves(datetime.min, datetime.min)
        self._assert_inserting_infinity_end_time_retrieves(
            datetime.max.replace(tzinfo=timezone.get_default_timezone()), datetime.max
        )
        self._assert_inserting_infinity_end_time_retrieves(
            datetime.min.replace(tzinfo=timezone.get_default_timezone()), datetime.min
        )
        self._assert_inserting_infinity_end_time_retrieves("infinity", datetime.max)
        self._assert_inserting_infinity_end_time_retrieves("-infinity", datetime.min)

    def test_inserting_illegal_values_fails(self):
        self.event1.end_time = "illegal"
        with self.assertRaises(ValidationError):
            self.event1.save()

    def _assert_inserting_standard_datetime_end_time_retrieves_the_same(self, insert_value):
        insert_value = make_aware(insert_value)
        self._save_end_time(self.event1, insert_value)
        self.event1.refresh_from_db()
        if insert_value is not None:
            self.assertTrue(is_aware(self.event1.end_time))
        self.assertEqual(self.event1.end_time, insert_value)

    def test_inserting_standard_values_retrieves_the_same(self):
        self._save_end_time(self.event1, None)
        self.event1.refresh_from_db()
        self.assertEqual(self.event1.end_time, None)

        self._assert_inserting_standard_datetime_end_time_retrieves_the_same(datetime(2000, 1, 1))
        self._assert_inserting_standard_datetime_end_time_retrieves_the_same(datetime.now())
        self._assert_inserting_standard_datetime_end_time_retrieves_the_same(datetime.max - timedelta(days=1))
        self._assert_inserting_standard_datetime_end_time_retrieves_the_same(datetime.min + timedelta(days=1))

    def test_sorting_by_end_time_sorts_expectedly(self):
        self._save_end_time(self.event1, make_aware(datetime(2000, 1, 1)))
        self._save_end_time(self.event2, make_aware(datetime(1999, 12, 31)))
        self._save_end_time(self.event3, make_aware(datetime(2000, 1, 2)))
        self.assertListEqual(
            list(TestEvent.objects.order_by("end_time")), [self.event2, self.event1, self.event3]
        )

        self._save_end_time(self.event1, "-infinity")
        self._save_end_time(self.event2, make_aware(datetime(2000, 1, 1)))
        self._save_end_time(self.event3, "infinity")
        self.assertListEqual(
            list(TestEvent.objects.order_by("end_time")), [self.event1, self.event2, self.event3]
        )

    def test_filtering_on_end_time_filters_expectedly(self):
        end_time2 = make_aware(datetime(2000, 1, 1))
        self._save_end_time(self.event1, "-infinity")
        self._save_end_time(self.event2, end_time2)
        self._save_end_time(self.event3, "infinity")
        self.assertListEqual(
            list(TestEvent.objects.filter(end_time__gte=end_time2).order_by("end_time")),
            [self.event2, self.event3],
        )
        self.assertListEqual(
            list(TestEvent.objects.filter(end_time__lte=end_time2).order_by("end_time")),
            [self.event1, self.event2],
        )

        self.assertListEqual(
            list(TestEvent.objects.filter(end_time__gte="-infinity").order_by("end_time")),
            [self.event1, self.event2, self.event3],
        )
        self.assertListEqual(
            list(TestEvent.objects.filter(end_time__lte="infinity").order_by("end_time")),
            [self.event1, self.event2, self.event3],
        )

        self.assertFalse(TestEvent.objects.filter(end_time__lt="-infinity").exists())
        self.assertFalse(TestEvent.objects.filter(end_time__gt="infinity").exists())
