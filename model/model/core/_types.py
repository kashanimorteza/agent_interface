"""Field Type realization (private): the closed Field Type set and its forms."""

import datetime
import math
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import UUID


class FieldType(StrEnum):
    string = "string"
    integer = "integer"
    float = "float"
    decimal = "decimal"
    boolean = "boolean"
    datetime = "datetime"
    date = "date"
    time = "time"
    uuid = "uuid"


def parse_field_type(value: object) -> FieldType:
    """Return the Field Type named by value; any other Type is refused."""
    if isinstance(value, FieldType):
        return value
    try:
        return FieldType(value)
    except ValueError:
        known = ", ".join(FieldType)
        raise ValueError(
            f"Unknown Field Type {value!r}; the Field Types are {known}"
        ) from None


def is_valid_value(field_type: FieldType, value: object) -> bool:
    """Whether value is exactly the Python representation of the Field Type."""
    match field_type:
        case FieldType.string:
            return isinstance(value, str)
        case FieldType.integer:
            return isinstance(value, int) and not isinstance(value, bool)
        case FieldType.float:
            return isinstance(value, float) and math.isfinite(value)
        case FieldType.decimal:
            return isinstance(value, Decimal) and value.is_finite()
        case FieldType.boolean:
            return isinstance(value, bool)
        case FieldType.datetime:
            return (
                isinstance(value, datetime.datetime) and value.utcoffset() is not None
            )
        case FieldType.date:
            return isinstance(value, datetime.date) and not isinstance(
                value, datetime.datetime
            )
        case FieldType.time:
            return isinstance(value, datetime.time)
        case FieldType.uuid:
            return isinstance(value, UUID)


def to_json_value(field_type: FieldType, value: Any) -> Any:
    """Return the JSON form of a value of the Field Type."""
    if value is None:
        return None
    match field_type:
        case FieldType.decimal | FieldType.uuid:
            return str(value)
        case FieldType.datetime | FieldType.date | FieldType.time:
            return value.isoformat()
        case _:
            return value


def from_json_value(field_type: FieldType, value: Any) -> Any:
    """Return the Python form of a decoded JSON value of the Field Type."""
    if isinstance(value, int) and not isinstance(value, bool):
        return float(value) if field_type is FieldType.float else value
    if not isinstance(value, str):
        return value
    try:
        match field_type:
            case FieldType.decimal:
                return Decimal(value)
            case FieldType.datetime:
                return datetime.datetime.fromisoformat(value)
            case FieldType.date:
                return datetime.date.fromisoformat(value)
            case FieldType.time:
                return datetime.time.fromisoformat(value)
            case FieldType.uuid:
                return UUID(value)
            case _:
                return value
    except ArithmeticError, ValueError:
        raise ValueError(f"The text is not a valid {field_type} form") from None
