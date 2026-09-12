"""Derives request and response schemas for a Model from Model Interface,
excluding every Credential field from every response shape.

Deliberately does NOT use `from __future__ import annotations`: FastAPI must
resolve these dynamically built, per-request-parameterized types at runtime,
and postponed evaluation would turn their annotations into unresolvable
string forward references.
"""

from typing import Any

from pydantic import BaseModel, Field, create_model

from my_backend._model_interface import BaseModel as ModelBaseModel
from my_backend._model_interface import credential_field_names


def build_schemas(model_type: type[ModelBaseModel]) -> tuple[type[BaseModel], type[BaseModel], type[BaseModel]]:
    """Returns (CreateSchema, UpdateSchema, ReadSchema) for ``model_type``.

    CreateSchema: every field except the server-assigned ``id``, with its
    original constraints preserved; a Credential field is accepted here as
    write-only input.

    UpdateSchema: every field except ``id``, all made optional for partial
    updates. The full resulting state is still re-validated against the
    Model by Database Interface before it is committed, so relaxing
    per-field constraints here (an implementation choice) never weakens the
    guarantee that only a valid complete record is ever persisted.

    ReadSchema: every field except every Credential field, which Backend
    Principle 10 requires excluding from every response and response schema.
    """

    credential_names = credential_field_names(model_type)
    fields = model_type.model_fields

    create_fields: dict[str, Any] = {
        name: (field.annotation, field) for name, field in fields.items() if name != "id"
    }
    update_fields: dict[str, Any] = {
        name: (field.annotation | None if field.annotation is not None else None, Field(default=None))
        for name, field in fields.items()
        if name != "id"
    }
    read_fields: dict[str, Any] = {
        name: (field.annotation, field)
        for name, field in fields.items()
        if name not in credential_names
    }

    create_schema = create_model(f"{model_type.__name__}Create", **create_fields)
    update_schema = create_model(f"{model_type.__name__}Update", **update_fields)
    read_schema = create_model(f"{model_type.__name__}Read", **read_fields)
    return create_schema, update_schema, read_schema
