"""Public Foundation contract: lossless conversion between an Entity and JSON text."""

import json
from collections.abc import Callable
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, NoReturn, Self
from uuid import UUID

from model.core.base import Base, reconstructing

_PARSERS: dict[str, Callable[[str], Any]] = {
    "decimal": Decimal,
    "datetime": datetime.fromisoformat,
    "date": date.fromisoformat,
    "time": time.fromisoformat,
    "uuid": UUID,
}


def _reject_constant(constant: str) -> NoReturn:
    raise ValueError("JSON text must conform to the JSON standard")


def _parse(parser: Callable[[str], Any], value: Any) -> Any:
    """Parse a JSON string into its declared category; validation rejects the rest."""
    if not isinstance(value, str):
        return value
    try:
        return parser(value)
    except (ArithmeticError, ValueError):
        return value


class Foundation(Base):
    """Convert an Entity to and from JSON text.

    The text has one object at its root whose keys are the Entity's Field names in
    Declaration order.
    """

    def to_json(self) -> str:
        """Convert the Entity to JSON text."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Rebuild an Entity from JSON text under the Field contracts of construction.

        A null generated Field stays pending; a generated value restores an assigned
        identity.
        """
        data = json.loads(text, parse_constant=_reject_constant)
        if not isinstance(data, dict):
            raise ValueError("JSON text must have one object at its root")
        for declared in cls.declaration.fields:
            if declared.type in _PARSERS and declared.name in data:
                parser = _PARSERS[declared.type]
                data[declared.name] = _parse(parser, data[declared.name])
        token = reconstructing.set(True)
        try:
            return cls(**data)
        finally:
            reconstructing.reset(token)
