from django.db import models

from django_pg_infinity.fields import DateTimeInfinityField


class TestEvent(models.Model):
    name = models.CharField(max_length=100, default="test")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = DateTimeInfinityField(null=True, blank=True)

    class Meta:
        app_label = "tests"
