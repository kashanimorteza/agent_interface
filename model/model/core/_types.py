"""Private Field Type realization: Python values and JSON forms of the closed Field Types.

Types are keyed by the string value of a Field Type, so this module stays independent of the
public Declaration contract.
"""

import math
from collections.abc import Callable
from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import AwareDatetime

PYTHON_TYPES: dict[str, type] = {
    "string": str,
    "integer": int,
    "float": float,
    "decimal": Decimal,
    "boolean": bool,
    "datetime": datetime,
    "date": date,
    "time": time,
    "uuid": UUID,
}

ANNOTATIONS: dict[str, object] = {
    "string": str,
    "integer": int,
    "float": float,
    "decimal": Decimal,
    "boolean": bool,
    "datetime": AwareDatetime,
    "date": date,
    "time": time,
    "uuid": UUID,
}


def accepts(field_type: str, value: object) -> bool:
    """Whether a value is a valid, non-null value of the Field Type, without coercion."""
    match field_type:
        case "string" | "uuid" | "time":
            return isinstance(value, PYTHON_TYPES[field_type])
        case "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        case "float":
            return isinstance(value, float) and math.isfinite(value)
        case "decimal":
            return isinstance(value, Decimal) and value.is_finite()
        case "boolean":
            return isinstance(value, bool)
        case "datetime":
            return isinstance(value, datetime) and value.utcoffset() is not None
        case "date":
            return isinstance(value, date) and not isinstance(value, datetime)
    raise ValueError(f"Unknown Field Type: {field_type!r}")


def to_json_value(field_type: str, value: object) -> object:
    """The JSON form of a non-null value."""
    match field_type:
        case "string" | "integer" | "boolean":
            return value
        case "float":
            if not (isinstance(value, float) and math.isfinite(value)):
                raise ValueError("A float must be finite.")
            return value
        case "decimal":
            return str(value)
        case "datetime" | "date" | "time":
            if isinstance(value, date | time):
                return value.isoformat()
            raise ValueError(f"Not a {field_type} value.")
        case "uuid":
            return str(value)
    raise ValueError(f"Unknown Field Type: {field_type!r}")


def from_json_value(field_type: str, raw: object) -> object:
    """The Python value of the JSON form of a non-null value; raises ValueError without echoing it."""
    try:
        match field_type:
            case "string":
                return _text(raw)
            case "integer":
                if type(raw) is not int:
                    raise ValueError
                return raw
            case "float":
                if type(raw) is not int and type(raw) is not float:
                    raise ValueError
                return float(raw)
            case "boolean":
                if type(raw) is not bool:
                    raise ValueError
                return raw
            case "decimal":
                value = Decimal(_text(raw))
                if not value.is_finite():
                    raise ValueError
                return value
            case "datetime":
                value = datetime.fromisoformat(_text(raw))
                if value.utcoffset() is None:
                    raise ValueError
                return value
            case "date":
                return date.fromisoformat(_text(raw))
            case "time":
                return time.fromisoformat(_text(raw))
            case "uuid":
                return UUID(_text(raw))
    except ValueError, ArithmeticError:
        raise ValueError(f"Not a valid JSON form of a {field_type} value.") from None
    raise ValueError(f"Unknown Field Type: {field_type!r}")


def _text(raw: object) -> str:
    if type(raw) is not str:
        raise ValueError
    return raw


def identifier_factory(field_type: str) -> Callable[[], UUID | str]:
    """The producer of a Generated Identifier, using the algorithm Model Preferences select (uuid4)."""
    if field_type == "uuid":
        return uuid4
    if field_type == "string":
        return lambda: str(uuid4())
    raise ValueError("A Generated Identifier requires a uuid or string Field.")
