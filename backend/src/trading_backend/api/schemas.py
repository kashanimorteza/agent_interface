"""Pydantic schemas derived from the shared Model specifications.

For every Model: <Model>Create (all writable fields; credentials accepted as write-only input),
<Model>Update (every writable field optional for partial updates), and <Model>Read (every
non-credential field including the primary key). Create and Update forbid unknown fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, create_model

from trading_backend.logic.model_specs import MODEL_SPECS, FieldSpec, ModelSpec

TYPE_MAP: dict[str, type] = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "decimal": Decimal,
    "float": float,
    "datetime": datetime,
}


@dataclass(frozen=True)
class Schemas:
    create: type[BaseModel]
    update: type[BaseModel]
    read: type[BaseModel]


def pascal(key: str) -> str:
    return "".join(part.capitalize() for part in key.split("_"))


def _field_kwargs(field: FieldSpec) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if field.purpose:
        kwargs["description"] = field.purpose
    if field.size is not None and field.type == "string":
        kwargs["max_length"] = field.size
    return kwargs


def build_schemas(spec: ModelSpec) -> Schemas:
    """Create, Update, and Read schemas for one Model specification."""
    create_fields: dict[str, Any] = {}
    update_fields: dict[str, Any] = {}
    read_fields: dict[str, Any] = {}
    for field in spec.fields:
        py_type = TYPE_MAP[field.type]
        kwargs = _field_kwargs(field)
        if not field.primary_key:
            if field.nullable:
                create_fields[field.name] = (py_type | None, Field(default=None, **kwargs))
            elif field.has_default:
                create_fields[field.name] = (py_type, Field(default=field.default, **kwargs))
            else:
                create_fields[field.name] = (py_type, Field(**kwargs))
            update_fields[field.name] = (py_type | None, Field(default=None, **kwargs))
        if not field.credential:
            if field.nullable:
                read_fields[field.name] = (py_type | None, Field(default=None, **kwargs))
            else:
                read_fields[field.name] = (py_type, Field(**kwargs))
    name = pascal(spec.key)
    strict = ConfigDict(extra="forbid")
    return Schemas(
        create=create_model(f"{name}Create", __config__=strict, **create_fields),
        update=create_model(f"{name}Update", __config__=strict, **update_fields),
        read=create_model(f"{name}Read", **read_fields),
    )


SCHEMAS: dict[str, Schemas] = {key: build_schemas(spec) for key, spec in MODEL_SPECS.items()}
