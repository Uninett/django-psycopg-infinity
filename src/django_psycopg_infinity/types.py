from datetime import datetime, timedelta


__all__ = [
    "Infinity",
    "MinusInfinity",
]


class __infinity:
    _positive: bool
    _template: datetime

    def __new__(cls, *_, **kwargs):
        dt = cls._template
        args = (dt.year, dt.month, dt.day)
        kwargs = kwargs.copy()
        kwargs.update(
            dict(
                hour=dt.hour,
                second=dt.second,
                microsecond=dt.microsecond,
            )
        )
        return datetime.__new__(cls, *args, **kwargs)

    def __hash__(self):
        return hash((self._positive, str(self._template)))

    def __neg__(self):
        return self.__class__(not self.positive)

    # __ne__ reuses __eq__
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if not hasattr(other, "_positive"):
            return False
        return other._positive == self._positive

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self == other:
            return False
        return self._positive

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if isinstance(other, self):
            return True
        return False

    def __lt__(self, other):
        if not isinstance(other, self._template.__class__):
            return NotImplemented
        return not self._positive

    def __le__(self, other):
        if not isinstance(other, self._template.__class__):
            return NotImplemented
        return False

    def __bool__(self):
        return True

    def __nonzero__(self):
        return True

    def __str__(self):
        prefix = "" if self._positive else "-"
        return f"{prefix}infinity"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if isinstance(other, timedelta):
            return self
        if isinstance(other, self._template.__class__):
            return timedelta(0)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self
        if isinstance(other, self._template.__class__):
            return timedelta(0)
        return NotImplemented

    def __rsub__(self, other):
        return self.__sub__(other)


class __infinity_plus_datetime(__infinity, datetime):
    _positive = True
    _template = datetime.max


class __infinity_minus_datetime(__infinity, datetime):
    _positive = False
    _template = datetime.min


Infinity = __infinity_plus_datetime()
MinusInfinity = __infinity_minus_datetime()
