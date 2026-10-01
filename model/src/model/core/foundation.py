"""Shared conversion between an Entity and its JSON Object, as JSON text."""

import json
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from functools import cache, partial
from typing import Any, ClassVar, Self

from pydantic import ConfigDict, TypeAdapter

from model.core.declaration import Declaration
from model.core.diagnostics import strictly
from model.core.naming import field_name
from model.core.types import python_type

_reconstructing: ContextVar[bool] = ContextVar("entity_reconstructing", default=False)
_STRICT = ConfigDict(strict=True, hide_input_in_errors=True)


def reconstructing() -> bool:
    """Whether an Entity is being rebuilt from its JSON text."""
    return _reconstructing.get()


@contextmanager
def _reconstruction() -> Iterator[None]:
    token = _reconstructing.set(True)
    try:
        yield
    finally:
        _reconstructing.reset(token)


def _json_value(type_name: str, value: Any) -> Any:
    if value is None:
        return None
    if type_name in ("datetime", "date", "time"):
        return value.isoformat()
    if type_name in ("decimal", "uuid"):
        return str(value)
    return value


@cache
def _json_adapter(type_name: str) -> TypeAdapter[Any]:
    return TypeAdapter(python_type(type_name), config=_STRICT)


def _reject_constant(name: str) -> Any:
    raise ValueError(f"{name} is not valid JSON.")


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    if repeated:
        raise ValueError(f"JSON keys are repeated: {repeated}.")
    return dict(pairs)


class Foundation:
    """Converts an Entity to JSON text and back without loss."""

    declaration: ClassVar[Declaration]

    def to_json(self) -> str:
        """Return JSON text: one object whose keys are the Fields in Declaration order."""
        document = {
            field.name: _json_value(field.type, getattr(self, field_name(field.name)))
            for field in self.declaration.fields
        }
        return json.dumps(document, allow_nan=False, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Rebuild an Entity from JSON text produced by to_json, rejecting anything else."""
        document = json.loads(
            text, parse_constant=_reject_constant, object_pairs_hook=_object
        )
        if not isinstance(document, dict):
            raise TypeError("A JSON object is required.")
        declared = {field.name: field for field in cls.declaration.fields}
        unknown = sorted(set(document) - set(declared))
        if unknown:
            raise ValueError(f"JSON keys are not Fields: {unknown}.")
        values: dict[str, Any] = {}
        for key, raw in document.items():
            if raw is None:
                values[field_name(key)] = None
                continue
            type_name = declared[key].type
            if type_name == "decimal" and not isinstance(raw, str):
                raise ValueError(f"JSON key {key!r} must be the exact decimal text.")
            adapter = _json_adapter(type_name)
            values[field_name(key)] = strictly(
                partial(adapter.validate_json, json.dumps(raw))
            )
        with _reconstruction():
            return cls(**values)
