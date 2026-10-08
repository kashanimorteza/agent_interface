"""Foundation (public): the contract every Entity extends, with JSON conversion."""

import json
from typing import Any, Self

from model.core._base import Base
from model.core._types import from_json_value, to_json_value
from model.core.declaration import ValueGeneration

__all__ = ["Foundation"]


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError("The JSON text repeats a key")
    return dict(pairs)


def _refuse_constant(constant: str) -> Any:
    raise ValueError(f"The JSON text uses the non-standard constant {constant}")


class Foundation(Base):
    def to_json(self) -> str:
        """Return the JSON text of this Entity, keyed by its Fields in order."""
        values = {
            item.name: to_json_value(item.type, getattr(self, item.name))
            for item in type(self).declaration.fields
        }
        return json.dumps(values, allow_nan=False)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Return the Entity the JSON text describes."""
        data = json.loads(
            text, object_pairs_hook=_unique_pairs, parse_constant=_refuse_constant
        )
        if not isinstance(data, dict):
            raise TypeError("The JSON text must have one object at its root")
        specs = {item.name: item for item in cls.declaration.fields}
        values: dict[str, Any] = {}
        for key, value in data.items():
            spec = specs.get(key)
            if spec is None:
                values[key] = value
            elif (
                value is None
                and spec.value_generation is ValueGeneration.auto_increment
            ):
                continue
            else:
                try:
                    values[key] = from_json_value(spec.type, value)
                except ValueError as error:
                    raise ValueError(f"{key}: {error}") from None
        return cls(**values)
