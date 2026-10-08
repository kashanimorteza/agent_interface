"""Private Field Type realization: Python form, JSON text form and column form of every Field Type."""

from datetime import UTC, date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID

from pydantic import AwareDatetime
from sqlalchemy import DateTime, String
from sqlalchemy.types import TypeDecorator

from model.core.declaration import DeclarationError, FieldType, value_class


def annotation(field_type: FieldType, nullable: bool) -> Any:
    """Return the Python annotation of a Field: its Type, joined with None when nullable."""
    base = (
        AwareDatetime if field_type is FieldType.datetime else value_class(field_type)
    )
    return base | None if nullable else base


def json_encode(field_type: FieldType, value: Any) -> Any:
    """Return the JSON form of a value: decimals as exact text, temporal values and uuids as text."""
    if value is None:
        return None
    match field_type:
        case FieldType.decimal | FieldType.uuid:
            return str(value)
        case FieldType.datetime | FieldType.date | FieldType.time:
            return value.isoformat()
        case _:
            return value


def json_decode(field_type: FieldType, raw: Any) -> Any:
    """Return the Python form of a decoded JSON value.

    Text forms are converted by Type; any value that is not a valid text form is passed on unchanged so
    that strict validation refuses it.
    """
    if raw is None:
        return None
    match field_type:
        case FieldType.float:
            return (
                float(raw)
                if isinstance(raw, int) and not isinstance(raw, bool)
                else raw
            )
        case (
            FieldType.decimal
            | FieldType.datetime
            | FieldType.date
            | FieldType.time
            | FieldType.uuid
        ):
            if not isinstance(raw, str):
                return raw
            parse = {
                FieldType.decimal: Decimal,
                FieldType.datetime: datetime.fromisoformat,
                FieldType.date: date.fromisoformat,
                FieldType.time: time.fromisoformat,
                FieldType.uuid: UUID,
            }[field_type]
            try:
                return parse(raw)
            except ValueError, InvalidOperation:
                return raw
        case _:
            return raw


class DecimalText(TypeDecorator[Decimal]):
    """Stores a decimal as its exact text and returns a decimal on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, Decimal):
            raise DeclarationError("A decimal column accepts only decimal values.")
        return str(value)

    def process_result_value(self, value: str | None, dialect: Any) -> Decimal | None:
        return None if value is None else Decimal(value)


class AwareDateTime(TypeDecorator[datetime]):
    """Stores a datetime in UTC and reads it back timezone-aware, also where an Engine drops the offset."""

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(
        self, value: datetime | None, dialect: Any
    ) -> datetime | None:
        if value is None:
            return None
        if value.utcoffset() is None:
            raise DeclarationError(
                "A datetime column accepts only timezone-aware values."
            )
        return value.astimezone(UTC)

    def process_result_value(
        self, value: datetime | None, dialect: Any
    ) -> datetime | None:
        if value is None:
            return None
        return (
            value.replace(tzinfo=UTC)
            if value.utcoffset() is None
            else value.astimezone(UTC)
        )


def column_type(field_type: FieldType) -> Any:
    """Return the explicit column type of a Field Type, or None when the library default applies."""
    match field_type:
        case FieldType.decimal:
            return DecimalText
        case FieldType.datetime:
            return AwareDateTime
        case _:
            return None
