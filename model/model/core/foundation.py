"""Public Foundation contract: the shared conversion between an Entity and its JSON Object."""

import json
from typing import Any, Self

from model.core import _types
from model.core._base import Base


def _reject_repeated_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    document: dict[str, Any] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"The JSON text repeats the key {key!r}.")
        document[key] = value
    return document


def _reject_constant(constant: str) -> Any:
    raise ValueError("The JSON text holds a non-standard constant.")


class Foundation(Base):
    """What every Entity extends: Validation from Base and Conversion to and from JSON text."""

    def to_json(self) -> str:
        """The JSON text of this Entity: one root object whose keys are its Field names in Declaration order."""
        document: dict[str, object] = {}
        for field in self.declaration.fields:
            value = getattr(self, field.name)
            document[field.name] = (
                None if value is None else _types.to_json_value(field.type, value)
            )
        return json.dumps(document, allow_nan=False, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Build an Entity from JSON text, with the same rules as direct construction."""
        document = json.loads(
            text,
            object_pairs_hook=_reject_repeated_keys,
            parse_constant=_reject_constant,
        )
        if type(document) is not dict:
            raise ValueError("The JSON text must hold one root object.")
        fields = {field.name: field for field in cls.declaration.fields}
        values: dict[str, Any] = {}
        failure: str | None = None
        for key, raw in document.items():
            field = fields.get(key)
            if field is None or raw is None:
                values[key] = raw
                continue
            try:
                values[key] = _types.from_json_value(field.type, raw)
            except ValueError:
                failure = f"Field {key}: not a valid JSON form of a {field.type} value."
                break
        if failure is not None:
            raise ValueError(failure)
        return cls(**values)
