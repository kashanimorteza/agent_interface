"""Input and output representations derived from the shared Models.

Nothing here redefines a Model. Each representation is built from the
Model's own field declarations: the storage-assigned identifier is never an
input, a credential field is an input only, and every other property (type,
optionality, default, size) is carried over as declared.
"""

from __future__ import annotations

from typing import Any

from my_model import FieldSpec, Model
from pydantic import BaseModel, ConfigDict, Field, create_model

_cache: dict[tuple[type[Model], str], type[BaseModel]] = {}


def resource_name(model: type[Model]) -> str:
    """Plural kebab case of the Model name, for the transport."""
    words = _snake_case(model.__name__).split("_")
    words[-1] = _pluralize(words[-1])
    return "-".join(words)


def input_schema(model: type[Model], *, partial: bool = False) -> type[BaseModel]:
    """The fields a consumer supplies. ``partial`` makes every field optional
    for updates; an omitted field is left unchanged."""
    key = (model, "update" if partial else "create")
    if key not in _cache:
        fields: dict[str, Any] = {}
        for name, spec in model.field_specs().items():
            if spec.auto_increment and spec.primary_key:
                continue
            fields[name] = _field(spec, partial=partial)
        _cache[key] = create_model(
            f"{model.__name__}{'Update' if partial else 'Create'}",
            __config__=ConfigDict(extra="forbid"),
            **fields,
        )
    return _cache[key]


def output_schema(model: type[Model]) -> type[BaseModel]:
    """The fields a consumer receives: every field except credentials."""
    key = (model, "out")
    if key not in _cache:
        fields: dict[str, Any] = {}
        for name, spec in model.field_specs().items():
            if spec.credential:
                continue
            if spec.auto_increment and spec.primary_key:
                fields[name] = (spec.python_type, Field(description=spec.purpose or "The identifier."))
                continue
            fields[name] = _field(spec, partial=False)
        _cache[key] = create_model(f"{model.__name__}Out", __config__=ConfigDict(extra="ignore"), **fields)
    return _cache[key]


def _field(spec: FieldSpec, *, partial: bool) -> tuple[Any, Any]:
    annotation: Any = spec.python_type
    info: dict[str, Any] = {}
    if spec.purpose:
        info["description"] = spec.purpose
    if spec.size is not None:
        info["max_length"] = spec.size
    if partial or spec.nullable:
        annotation = annotation | None
    if partial:
        return annotation, Field(default=None, **info)
    if spec.has_default:
        return annotation, Field(default=spec.default, **info)
    if spec.nullable:
        return annotation, Field(default=None, **info)
    return annotation, Field(**info)


def _snake_case(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i and (not name[i - 1].isupper() or (i + 1 < len(name) and name[i + 1].islower())):
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def _pluralize(word: str) -> str:
    if word.endswith("y") and word[-2:-1] not in "aeiou":
        return word[:-1] + "ies"
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    return word + "s"
