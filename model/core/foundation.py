import re
from collections.abc import Mapping
from contextlib import suppress
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, ClassVar, Self, TypeGuard, cast

from pydantic import JsonValue

from .declaration import Declaration, FieldDeclaration
from .logical_type import LogicalType

_DECIMAL = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", re.ASCII)
_DATETIME = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?"
    r"(?:Z|[+-]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?)?",
    re.ASCII,
)


def _encode(field: FieldDeclaration, value: Any) -> JsonValue:
    if value is None:
        return None
    match field.type:
        case LogicalType.DECIMAL:
            return str(value)
        case LogicalType.DATETIME:
            return value.isoformat()
        case _:
            return value


def _decode(entity: str, field: FieldDeclaration, value: Any) -> Any:
    if value is None:
        return None
    match field.type:
        case LogicalType.DECIMAL | LogicalType.DATETIME:
            if not isinstance(value, str):
                raise TypeError(f"{entity}.{field.name}: {field.type} must be encoded as a string")
            pattern, parse = (
                (_DECIMAL, Decimal)
                if field.type is LogicalType.DECIMAL
                else (_DATETIME, datetime.fromisoformat)
            )
            if pattern.fullmatch(value):
                with suppress(ArithmeticError, ValueError):
                    return parse(value)
            raise ValueError(f"{entity}.{field.name}: invalid {field.type} encoding")
        case LogicalType.FLOAT if isinstance(value, int) and not isinstance(value, bool):
            with suppress(OverflowError):
                if float(value) == value:
                    return float(value)
            raise ValueError(
                f"{entity}.{field.name}: integer is not exactly representable as float"
            )
        case _:
            return value


def _is_json_object(data: Any) -> TypeGuard[Mapping[str, Any]]:
    return isinstance(data, Mapping) and all(
        isinstance(key, str) for key in cast("Mapping[Any, Any]", data)
    )


class Foundation:
    """Shared conversion of an Entity to and from its portable JSON representation.

    Attributes:
        declaration (Declaration): Declaration of the converting Entity.
    """

    declaration: ClassVar[Declaration]

    if TYPE_CHECKING:

        def __init__(self, **data: Any) -> None: ...

    def to_json(self) -> dict[str, JsonValue]:
        """Convert the Entity to a JSON object keyed by Field name in Declaration order.

        Returns:
            (dict[str, JsonValue]): Current value of every Field, with decimal as an exact
                base-10 string and datetime as ISO 8601 text.
        """
        return {
            field.name: _encode(field, getattr(self, field.name))
            for field in self.declaration.fields
        }

    @classmethod
    def from_json(cls, data: Any) -> Self:
        """Construct an Entity from a JSON object under the same contract as direct creation.

        Args:
            data (Any): JSON object keyed by Field name. A decimal is a base-10 string, a datetime
                is an ISO 8601 date-time string (YYYY-MM-DDTHH:MM[:SS[.ffffff]] with an optional
                Z or offset), and an exactly representable JSON integer is read as a float for a
                float Field.

        Returns:
            (Self): The constructed Entity.
        """
        if not _is_json_object(data):
            raise ValueError(f"{cls.declaration.name}: a JSON object with string keys is required")
        fields = {field.name: field for field in cls.declaration.fields}
        return cls(
            **{
                key: _decode(cls.declaration.name, fields[key], value) if key in fields else value
                for key, value in data.items()
            }
        )
