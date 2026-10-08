"""Public Foundation contract: lossless conversion between an Entity and its JSON text."""

import json
from typing import Any, Self

from model.core import _types
from model.core._base import Base
from model.core.declaration import ValueGeneration


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError("The JSON text repeats a key.")
    return dict(pairs)


def _reject_constant(name: str) -> Any:
    raise ValueError(f"The JSON text uses the non-standard constant {name}.")


def _finite_float(text: str) -> float:
    value = float(text)
    if value in (float("inf"), float("-inf")):
        raise ValueError("The JSON text holds a number outside the finite range.")
    return value


class Foundation(Base):
    """The public contract every Entity extends: conversion to and from its JSON text."""

    def to_json(self) -> str:
        """Return JSON text with one root object whose keys are the Field names in Declaration order."""
        data = {
            field.name: _types.json_encode(field.type, getattr(self, field.name))
            for field in self.declaration.fields
        }
        return json.dumps(data, allow_nan=False, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Rebuild an Entity from JSON text under the same rules as direct construction."""
        if not isinstance(text, str):
            raise TypeError("An Entity is rebuilt only from JSON text.")
        decoded = json.loads(
            text,
            object_pairs_hook=_unique_keys,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
        )
        if not isinstance(decoded, dict):
            raise TypeError("The JSON text must have one object at its root.")
        fields = {field.name: field for field in cls.declaration.fields}
        values: dict[str, Any] = {}
        for key, item in decoded.items():
            field = fields.get(key)
            if field is None:
                values[key] = item
            elif (
                field.value_generation is ValueGeneration.auto_increment
                and item is None
            ):
                continue
            else:
                values[key] = _types.json_decode(field.type, item)
        return cls(**values)

    @classmethod
    def model_validate_json(cls, json_data: Any, **kwargs: Any) -> Self:
        return cls.from_json(json_data)
