from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, ClassVar, Self, TypeGuard, cast

from pydantic import JsonValue

from .declaration import Declaration, FieldDeclaration
from .logical_type import LogicalType


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
            parse = Decimal if field.type is LogicalType.DECIMAL else datetime.fromisoformat
            if not isinstance(value, str):
                raise TypeError(f"{entity}.{field.name}: {field.type} must be encoded as a string")
            try:
                return parse(value)
            except ArithmeticError, ValueError:
                raise ValueError(f"{entity}.{field.name}: invalid {field.type} encoding") from None
        case LogicalType.FLOAT if isinstance(value, int) and not isinstance(value, bool):
            if float(value) != value:
                raise ValueError(
                    f"{entity}.{field.name}: integer is not exactly representable as float"
                )
            return float(value)
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
            data (Any): JSON object keyed by Field name; decimal and datetime are encoded as strings.

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
