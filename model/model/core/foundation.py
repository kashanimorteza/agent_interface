"""The public Foundation contract: lossless conversion between an Entity and its JSON Object.

The JSON Object is JSON text with one root object whose keys are exactly the Entity's Field
names, in Declaration order.
"""

import json
from typing import Any, NoReturn, Self

from model.core._base import Base
from model.core._types import decode_json


def _refuse_constant(constant: str) -> NoReturn:
    raise ValueError(f"{constant} is not JSON")


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("a key is repeated in the JSON object")
    return result


class Foundation(Base):
    """Base of every Entity, adding conversion to and from its JSON Object."""

    def to_json(self) -> str:
        """Return the Entity as JSON text conforming to the JSON standard."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Reconstruct an Entity from JSON text, enforcing the same rules as direct construction.

        Malformed text, a repeated key, or a root that is not one object is rejected.
        """
        data = json.loads(text, parse_constant=_refuse_constant, object_pairs_hook=_object)
        if not isinstance(data, dict):
            raise ValueError("the JSON text must hold one object")
        types = {field.name: field.type for field in cls.declaration.fields}
        values = {
            key: decode_json(types[key], value) if key in types else value
            for key, value in data.items()  # pyright: ignore[reportUnknownVariableType]
        }
        return cls(**values)
