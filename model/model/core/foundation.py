"""Foundation: the public shared contract every Entity extends, converting it to and from JSON text."""

import json
from math import isfinite
from typing import Any, Self

from ._base import Base
from ._types import decode_json_value, encode_json_value
from .declaration import ValueGeneration


def _reject_constant(constant: str) -> Any:
    raise ValueError("JSON text must not contain a non-standard constant")


def _finite_float(text: str) -> float:
    number = float(text)
    if not isfinite(number):
        raise ValueError("JSON text must not contain a number outside the finite range")
    return number


def _object_without_repeats(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError("JSON text must not repeat a key")
    return dict(pairs)


class Foundation(Base):
    """Gives every Entity a lossless round trip through JSON text."""

    def to_json(self) -> str:
        """Return JSON text with one root object whose keys are the Field names, in Declaration order."""
        document = {
            item.name: encode_json_value(item.type, getattr(self, item.name))
            for item in type(self).declaration.fields
        }
        return json.dumps(document, allow_nan=False, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Build an Entity from JSON text, applying the same rules as direct construction."""
        if not isinstance(text, str):
            raise TypeError("JSON text must be a string")
        document = json.loads(
            text,
            object_pairs_hook=_object_without_repeats,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
        )
        if not isinstance(document, dict):
            raise TypeError("JSON text must have one object at its root")
        declared = {item.name: item for item in cls.declaration.fields}
        values: dict[str, Any] = {}
        for name, raw in document.items():
            item = declared.get(name)
            if item is None:
                values[name] = raw
            elif (
                item.value_generation == ValueGeneration.auto_increment and raw is None
            ):
                continue
            else:
                try:
                    values[name] = decode_json_value(item.type, raw)
                except TypeError, ValueError:
                    raise ValueError(
                        f"The JSON value of the Field {name!r} is not a valid {item.type} text form"
                    ) from None
        return cls(**values)
