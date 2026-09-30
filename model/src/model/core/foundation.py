"""Public Foundation contract: lossless Entity <-> JSON Object conversion.

A JSON Object is the decoded, JSON-compatible mapping of Field names to values. Text
encoding and decoding stay outside Model. Decimal values travel as strings and
datetime values as ISO 8601 strings, so nothing is lost or coerced.
"""

import re
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, ClassVar, Self

from sqlmodel import SQLModel

from model.core._failure import reject
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration

_DECIMAL_TEXT = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def _encode(declared: FieldDeclaration, value: Any) -> Any:
    if value is None:
        return None
    if declared.type == "decimal":
        return str(value)
    if declared.type == "datetime":
        return value.isoformat()
    return value


def _decode(entity: str, declared: FieldDeclaration, value: Any) -> Any:
    if value is None:
        return None
    if declared.type == "decimal":
        if not isinstance(value, str):
            raise reject(
                entity, declared.name, "malformed_value", "Decimal must be text."
            )
        try:
            number = Decimal(value)
        except InvalidOperation:
            number = None  # rejected below, outside the handler
        if number is None:
            raise reject(entity, declared.name, "malformed_value", "Not a decimal.")
        if not number.is_finite() or _DECIMAL_TEXT.fullmatch(value) is None:
            raise reject(
                entity, declared.name, "malformed_value", "Not a finite decimal."
            )
        return number
    if (
        declared.type == "float"
        and isinstance(value, int)
        and not isinstance(value, bool)
    ):
        try:
            approximation = float(value)
            exact = int(approximation) == value
        except OverflowError:
            approximation, exact = 0.0, False
        if not exact:
            raise reject(
                entity,
                declared.name,
                "malformed_value",
                "Integer is not exactly representable as a float.",
            )
        return approximation
    if declared.type == "datetime":
        if not isinstance(value, str):
            raise reject(
                entity, declared.name, "malformed_value", "Datetime must be text."
            )
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            pass  # raised below, outside the handler, so no context keeps the text
        raise reject(entity, declared.name, "malformed_value", "Not a datetime.")
    return value


class Foundation(SQLModel):
    """Shared conversion capabilities exposed by every Entity."""

    Declaration: ClassVar[EntityDeclaration]

    def to_json(self) -> dict[str, Any]:
        """Return the JSON Object: exactly the Field names, in Declaration order."""
        return {
            declared.name: _encode(declared, getattr(self, declared.name))
            for declared in self.Declaration.fields
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Self:
        """Rebuild an Entity from a JSON Object without loss.

        A generated Field that is null stays pending; a generated Field that holds a
        value is assigned once after construction, as its owner would assign it.
        """
        entity = cls.Declaration.name
        if not isinstance(data, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise reject(entity, None, "malformed_object", "Object must be a mapping.")
        declared = {field.name: field for field in cls.Declaration.fields}
        for key in data:
            if key not in declared:
                raise reject(
                    entity, str(key), "unknown_field", "Field is not declared."
                )
        values: dict[str, Any] = {}
        generated: dict[str, Any] = {}
        for name, value in data.items():
            field = declared[name]
            if field.value_generation is None:
                values[name] = _decode(entity, field, value)
            elif value is not None:
                generated[name] = value
        entity_instance = cls(**values)
        for name, value in generated.items():
            setattr(entity_instance, name, value)
        return entity_instance
