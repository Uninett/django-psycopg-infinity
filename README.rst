====================
django-pg-infinity
====================

Django field and PostgreSQL backend for infinity timestamp support with psycopg3.

Maps PostgreSQL's ``infinity`` / ``-infinity`` timestamp values to
``datetime.max`` / ``datetime.min`` in Python, making them usable as
regular ``DateTimeField`` values in Django models.

Installation
============

.. code-block:: bash

    pip install django-pg-infinity

Configuration
=============

Set the custom database backend in your Django settings:

.. code-block:: python

    DATABASES = {
        "default": {
            "ENGINE": "django_pg_infinity.backends.postgresql",
            # ... other settings
        },
    }

Then use ``DateTimeInfinityField`` in your models:

.. code-block:: python

    from django.db import models
    from django_pg_infinity.fields import DateTimeInfinityField

    class MyModel(models.Model):
        valid_until = DateTimeInfinityField(null=True, blank=True)

Usage
=====

.. code-block:: python

    from datetime import datetime

    # Store positive infinity
    obj.valid_until = datetime.max
    obj.save()

    # Or use the string representation
    obj.valid_until = "infinity"
    obj.save()

    # Retrieve — always returns an aware datetime
    obj.refresh_from_db()
    assert obj.valid_until.replace(tzinfo=None) == datetime.max

Development
===========

Tests require a running PostgreSQL instance. Configure via environment variables:

.. code-block:: bash

    export POSTGRES_DB=django_pg_infinity_test
    export POSTGRES_USER=postgres
    export POSTGRES_HOST=localhost

    pip install -e ".[test]"
    python runtests.py

License
=======

GPL-3.0-or-later
