"""Field Type realization: the value form of every Field Type in Python and in a JSON Object."""

import keyword
import re
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from math import isfinite
from typing import Annotated, Any
from uuid import UUID, uuid4

from pydantic import AwareDatetime, BeforeValidator

PYTHON_TYPES: dict[str, Any] = {
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

JSON_FORMS: dict[str, str] = {
    "string": "string",
    "integer": "number",
    "float": "number",
    "decimal": "string",
    "boolean": "true / false",
    "datetime": "ISO 8601 string with offset",
    "date": "ISO 8601 date string",
    "time": "ISO 8601 time string",
    "uuid": "string",
}


class UnknownFieldTypeError(ValueError):
    """A Field Type outside the closed set was named."""


def _known(type_name: str) -> str:
    if type_name not in PYTHON_TYPES:
        raise UnknownFieldTypeError(f"Unknown Field Type: {type_name!r}")
    return type_name


def python_type(type_name: str) -> Any:
    """Return the Python type that realizes a Field Type."""
    return PYTHON_TYPES[_known(type_name)]


def json_form(type_name: str) -> str:
    """Return the JSON form that represents a Field Type."""
    return JSON_FORMS[_known(type_name)]


def matches(type_name: str, value: Any) -> bool:
    """Return whether a value is exactly of a Field Type, without coercion."""
    match _known(type_name):
        case "string":
            return isinstance(value, str)
        case "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        case "float":
            return isinstance(value, float) and isfinite(value)
        case "decimal":
            return isinstance(value, Decimal)
        case "boolean":
            return isinstance(value, bool)
        case "datetime":
            return isinstance(value, datetime) and value.utcoffset() is not None
        case "date":
            return isinstance(value, date) and not isinstance(value, datetime)
        case "time":
            return isinstance(value, time)
        case _:
            return isinstance(value, UUID)


def encode_json_value(type_name: str, value: Any) -> Any:
    """Return the JSON-ready form of a value of a Field Type."""
    if value is None:
        return None
    match _known(type_name):
        case "decimal" | "uuid":
            return str(value)
        case "datetime" | "date" | "time":
            return value.isoformat()
        case _:
            return value


def decode_json_value(type_name: str, value: Any) -> Any:
    """Return the Python value for the JSON text form of a Field Type."""
    if value is None:
        return None
    match _known(type_name):
        case "decimal" | "uuid" | "datetime" | "date" | "time" as known:
            if not isinstance(value, str):
                raise TypeError(f"Expected the text form of a {known} value")
            try:
                return {
                    "decimal": Decimal,
                    "uuid": UUID,
                    "datetime": datetime.fromisoformat,
                    "date": date.fromisoformat,
                    "time": time.fromisoformat,
                }[known](value)
            except (InvalidOperation, ValueError) as error:
                raise ValueError(f"Invalid text form of a {known} value") from error
        case _:
            return value


def generate_identifier(type_name: str) -> UUID | str:
    """Return a fresh Generated Identifier for a uuid or string Field."""
    identifier = uuid4()
    return identifier if _known(type_name) == "uuid" else str(identifier)


def entity_physical_name(logical_name: str) -> str:
    """Return the PascalCase physical name of an Entity, or fail when it cannot be resolved."""
    words = re.findall(r"[A-Za-z0-9]+", logical_name)
    physical = "".join(word[:1].upper() + word[1:] for word in words)
    if not physical.isidentifier() or keyword.iskeyword(physical):
        raise ValueError(f"The Entity name {logical_name!r} has no valid physical name")
    return physical


def _require_float(value: Any) -> Any:
    if not isinstance(value, float) or not isfinite(value):
        raise ValueError("Input should be a finite float")
    return value


FloatValue = Annotated[float, BeforeValidator(_require_float)]
