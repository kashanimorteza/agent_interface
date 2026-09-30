"""Shared, lossless conversion between an Entity and its JSON Object."""

import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, ClassVar, NoReturn, Self

from sqlmodel import SQLModel

from .declaration import Declaration, FieldType


def _reject_constant(constant: str) -> NoReturn:
    raise ValueError(f"{constant} is not valid JSON")


def _decode(name: str, field_type: FieldType | None, value: Any) -> Any:
    """Decode the JSON representation of a Field value into its declared Type."""
    if not isinstance(value, str):
        return value
    try:
        if field_type is FieldType.DECIMAL:
            return Decimal(value)
        if field_type is FieldType.DATETIME:
            return datetime.fromisoformat(value)
    except InvalidOperation, ValueError:
        raise ValueError(f"{name} is not a valid {field_type} value") from None
    return value


class Foundation(SQLModel):
    """Conversion capabilities every Entity exposes; Entities inherit them."""

    declaration: ClassVar[Declaration]

    def to_json(self) -> str:
        """Convert the Entity to JSON text with its Fields as the keys of one root object."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Reconstruct an Entity from the JSON text that to_json produces."""
        match json.loads(text, parse_constant=_reject_constant):
            case dict() as data:
                types = {f.name: f.type for f in cls.declaration.fields}
                return cls(
                    **{
                        name: _decode(name, types.get(name), value)
                        for name, value in data.items()
                    }
                )
            case _:
                raise ValueError("JSON text must hold one object at its root")
