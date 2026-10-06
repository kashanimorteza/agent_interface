"""Realization of the Field Types a Target can declare."""

import datetime
import decimal
import uuid
from enum import StrEnum
from typing import Annotated, Any

from pydantic import AllowInfNan, AwareDatetime


class FieldType(StrEnum):
    """The closed set of Field Types; any other Type is refused."""

    string = "string"
    integer = "integer"
    float = "float"
    decimal = "decimal"
    boolean = "boolean"
    datetime = "datetime"
    date = "date"
    time = "time"
    uuid = "uuid"


PYTHON_TYPES: dict[FieldType, type] = {
    FieldType.string: str,
    FieldType.integer: int,
    FieldType.float: float,
    FieldType.decimal: decimal.Decimal,
    FieldType.boolean: bool,
    FieldType.datetime: datetime.datetime,
    FieldType.date: datetime.date,
    FieldType.time: datetime.time,
    FieldType.uuid: uuid.UUID,
}

# A float must be finite: JSON has no form for NaN or infinity, so they would be lost.
FiniteFloat = Annotated[float, AllowInfNan(False)]

ANNOTATIONS: dict[FieldType, Any] = {
    **PYTHON_TYPES,
    FieldType.float: FiniteFloat,
    FieldType.datetime: AwareDatetime,
}

_JSON_DECODERS = {
    FieldType.decimal: decimal.Decimal,
    FieldType.datetime: datetime.datetime.fromisoformat,
    FieldType.date: datetime.date.fromisoformat,
    FieldType.time: datetime.time.fromisoformat,
    FieldType.uuid: uuid.UUID,
}


def decode_json(field_type: FieldType, value: Any) -> Any:
    """Turn the JSON text form of a value into its Python form.

    A value that is not the expected text form, or that cannot be decoded, is returned unchanged
    so that strict validation rejects it.
    """
    decoder = _JSON_DECODERS.get(field_type)
    if decoder is None or not isinstance(value, str):
        return value
    try:
        return decoder(value)
    except ValueError, ArithmeticError:
        return value
