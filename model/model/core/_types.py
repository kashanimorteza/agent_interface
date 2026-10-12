"""Private realization of the closed set of Field Types.

Types are keyed by their Field Type values, so this file depends on no other Core file.
"""

import datetime
import decimal
import math
import re
import uuid
from types import MappingProxyType
from typing import Any, Final

from pydantic import AwareDatetime

_REALIZATIONS: Final = MappingProxyType(
    {
        "string": str,
        "integer": int,
        "float": float,
        "decimal": decimal.Decimal,
        "boolean": bool,
        "datetime": AwareDatetime,
        "date": datetime.date,
        "time": datetime.time,
        "uuid": uuid.UUID,
    }
)

TEXT_FORMS: Final = frozenset({"decimal", "datetime", "date", "time", "uuid"})
"""The Field Types whose JSON form is a string."""


def annotation(field_type: str, *, optional: bool) -> Any:
    """The Python annotation that realizes a Field Type.

    An optional realization adds None, for a nullable Field or a pending Auto
    Increment value.
    """
    realized = _REALIZATIONS[field_type]
    return realized | None if optional else realized


_DECIMAL_TEXT: Final = re.compile(
    r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", re.ASCII
)

_DECODERS: Final = MappingProxyType(
    {
        "decimal": lambda text: (
            decimal.Decimal(text) if _DECIMAL_TEXT.fullmatch(text) else None
        ),
        "datetime": datetime.datetime.fromisoformat,
        "date": datetime.date.fromisoformat,
        "time": datetime.time.fromisoformat,
        "uuid": uuid.UUID,
    }
)


def decode_text(field_type: str, text: str) -> Any:
    """Decode the JSON text form of a decimal, datetime, date, time, or uuid value.

    Returns None when the text is not a valid ASCII form of the Type.
    """
    if not text.isascii():
        return None
    try:
        return _DECODERS[field_type](text)
    except ValueError:
        return None


def _is_string(value: object) -> bool:
    return type(value) is str


def _is_integer(value: object) -> bool:
    return type(value) is int


def _is_float(value: object) -> bool:
    return type(value) is float and math.isfinite(value)


def _is_decimal(value: object) -> bool:
    return type(value) is decimal.Decimal and value.is_finite()


def _is_boolean(value: object) -> bool:
    return type(value) is bool


def _is_datetime(value: object) -> bool:
    return isinstance(value, datetime.datetime) and value.utcoffset() is not None


def _is_date(value: object) -> bool:
    return type(value) is datetime.date


def _is_time(value: object) -> bool:
    return type(value) is datetime.time


def _is_uuid(value: object) -> bool:
    return type(value) is uuid.UUID


_CONFORMS: Final = MappingProxyType(
    {
        "string": _is_string,
        "integer": _is_integer,
        "float": _is_float,
        "decimal": _is_decimal,
        "boolean": _is_boolean,
        "datetime": _is_datetime,
        "date": _is_date,
        "time": _is_time,
        "uuid": _is_uuid,
    }
)


def conforms(field_type: str, value: object) -> bool:
    """Whether a non-null value belongs to a Field Type, without coercion."""
    return _CONFORMS[field_type](value)
