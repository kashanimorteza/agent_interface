"""Foundation: shared conversion between Entities and their JSON representation."""

from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, ClassVar, Self

from sqlmodel import SQLModel

from model.core.declaration import Declaration, FieldDeclaration, FieldType

type JsonValue = str | int | float | bool | None


class Foundation(SQLModel):
    """Conversion capabilities shared by every Entity.

    Attributes:
        declaration: Declaration of the Entity.
    """

    declaration: ClassVar[Declaration]

    def to_json(self) -> dict[str, JsonValue]:
        """Convert the Entity to a JSON object keyed by its Field names in Declaration order.

        Returns:
            (dict[str, JsonValue]): Current value of every Field; decimals and datetimes are text.
        """
        return {
            f.name: _encode(f, getattr(self, f.name)) for f in self.declaration.fields
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Self:
        """Construct an Entity from a JSON object under the direct construction contract.

        Args:
            data (Mapping[str, Any]): JSON object keyed by Field name.

        Returns:
            (Self): The constructed Entity.
        """
        name = cls.declaration.name
        if not isinstance(data, Mapping) or not all(
            isinstance(key, str) for key in data
        ):
            raise ValueError(f"{name}: JSON must be an object with text keys")
        fields = {f.name: f for f in cls.declaration.fields}
        errors: list[str] = []
        values: dict[str, Any] = {}
        for key, value in data.items():
            field = fields.get(key)
            try:
                values[key] = value if field is None else _decode(field, value)
            except TypeError, ValueError, InvalidOperation:
                errors.append(
                    f"{name}.{key}: is not a valid {field.type if field else 'value'} representation"
                )
        if errors:
            raise ValueError("\n".join(errors))
        return cls(**values)


def _encode(field: FieldDeclaration, value: Any) -> JsonValue:
    if value is None:
        return None
    match field.type:
        case FieldType.DECIMAL:
            return str(value)
        case FieldType.DATETIME:
            return value.isoformat()
    return value


def _decode(field: FieldDeclaration, value: Any) -> Any:
    if value is None:
        return None
    match field.type:
        case FieldType.DECIMAL:
            return Decimal(_text(value))
        case FieldType.DATETIME:
            return datetime.fromisoformat(_text(value))
    return value


def _text(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError
    return value
