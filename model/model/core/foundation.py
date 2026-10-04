"""Foundation: lossless conversion between an Entity and its JSON Object."""

import json
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, ClassVar, Self
from uuid import UUID

from model.core.declaration import Declaration


class Foundation:
    """Shared conversion capability of every Entity; relies on the Entity's own Declaration."""

    declaration: ClassVar[Declaration]

    def to_json(self) -> str:
        """Return the JSON text whose root object has exactly the Entity's Field names in Declaration order."""
        declaration = type(self).declaration
        values: dict[str, Any] = {}
        for field in declaration.fields:
            value = getattr(self, field.name)
            if value is None:
                values[field.name] = None
            elif field.type == "decimal":
                values[field.name] = format(value, "f")
            elif field.type in ("datetime", "date", "time"):
                values[field.name] = value.isoformat()
            elif field.type == "uuid":
                values[field.name] = str(value)
            else:
                values[field.name] = value
        return json.dumps(values, ensure_ascii=False, allow_nan=False)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Rebuild an Entity from JSON text produced by to_json, applying the strict construction rules."""
        declaration = cls.declaration
        try:
            raw = json.loads(text)
        except TypeError, ValueError:
            raise ValueError("Malformed JSON text.") from None
        if not isinstance(raw, dict):
            raise TypeError("JSON text must hold one object at its root.")
        by_name = {field.name: field for field in declaration.fields}
        values: dict[str, Any] = {}
        for key, value in raw.items():
            field = by_name.get(key)
            if field is None or value is None:
                values[key] = value
            elif field.type == "decimal":
                values[key] = _decode(value, field.name, Decimal)
            elif field.type in _PARSERS:
                values[key] = _decode(value, field.name, _PARSERS[field.type])
            else:
                values[key] = value
        return cls._from_values(values)

    @classmethod
    def _from_values(cls, values: dict[str, Any]) -> Self:
        raise NotImplementedError


_PARSERS: dict[str, Any] = {
    "datetime": datetime.fromisoformat,
    "date": date.fromisoformat,
    "time": time.fromisoformat,
    "uuid": UUID,
}


def _decode(value: Any, name: str, parse: Any) -> Any:
    if not isinstance(value, str):
        raise TypeError(f"Field '{name}' must be a JSON string.")
    try:
        return parse(value)
    except ValueError, ArithmeticError:
        raise ValueError(f"Field '{name}' holds an invalid value.") from None
