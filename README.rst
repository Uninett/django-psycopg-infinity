====================
django-psycopg-infinity
====================

Django field and PostgreSQL backend for infinity timestamp support with psycopg >=3.

Maps PostgreSQL's ``infinity`` / ``-infinity`` timestamp values to
``datetime.max`` / ``datetime.min`` in Python, making them usable as
regular ``DateTimeField`` values in Django models.

Currently only ``DateTimeField`` is supported. ``DateField`` and ``TimeField``
infinity values are not yet handled. Contributions welcome!

Installation
============

.. code-block:: bash

    pip install django-psycopg-infinity

Configuration
=============

Set the custom database backend in your Django settings:

.. code-block:: python

    DATABASES = {
        "default": {
            "ENGINE": "django_psycopg_infinity.backends.postgresql",
            # ... other settings
        },
    }

Then use ``DateTimeInfinityField`` in your models:

.. code-block:: python

    from django.db import models
    from django_psycopg_infinity.fields import DateTimeInfinityField

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

    # Retrieve - always returns an aware datetime
    obj.refresh_from_db()
    assert obj.valid_until.replace(tzinfo=None) == datetime.max

Development
===========

Tests require a running PostgreSQL instance:

.. code-block:: bash

    cp .env.example .env   # edit as needed
    uv run runtests.py

Releasing
=========

Releases are published to PyPI automatically when a version tag is pushed.
The CI runs the full test suite before publishing.

Create a new release on GitHub with a ``v``-prefixed tag (e.g. ``v0.1.0``)
and the workflow handles the rest.

Versioning is derived from git tags via ``hatch-vcs``, so there are no
version strings to update manually.

License
=======

Apache-2.0
