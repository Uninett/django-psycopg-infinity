"""Django field and PostgreSQL backend for infinity timestamp support with psycopg3."""

try:
    from django_psycopg_infinity._version import __version__
except ImportError:
    __version__ = "uninstalled"

__all__ = ["__version__"]
