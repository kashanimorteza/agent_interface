"""Derives Create, Update, and Read request/response schemas from a shared
Model definition. A Credential field is accepted only in Create and Update
and is never part of a Read schema, so it can never appear in a response.
"""

from __future__ import annotations

from functools import cache

import my_model as m
from pydantic import BaseModel, Field, create_model


@cache
def read_schema(model_type: type[m.BaseModel]) -> type[BaseModel]:
    """The public response shape: every field except Credential fields."""
    fields = {}
    for name, info in model_type.model_fields.items():
        if name in model_type.credential_fields:
            continue
        fields[name] = (info.annotation, Field(default=info.default))
    return create_model(f"{model_type.__name__}Read", **fields)


@cache
def create_schema(model_type: type[m.BaseModel]) -> type[BaseModel]:
    """The request shape for creating a record: every field except the
    server-generated identifier. A Credential field remains required or
    optional exactly as the Model declares it.
    """
    fields = {}
    for name, info in model_type.model_fields.items():
        if name == "id":
            continue
        if info.is_required():
            fields[name] = (info.annotation, Field())
        else:
            fields[name] = (info.annotation, Field(default=info.default))
    return create_model(f"{model_type.__name__}Create", **fields)


@cache
def update_schema(model_type: type[m.BaseModel]) -> type[BaseModel]:
    """The request shape for a partial update: every field except the
    identifier, all optional so an omitted field is left unchanged. Read
    with ``exclude_unset=True`` to distinguish omission from explicit null.
    """
    fields = {}
    for name, info in model_type.model_fields.items():
        if name == "id":
            continue
        annotation = info.annotation
        assert annotation is not None
        fields[name] = (annotation | None, Field(default=None))
    return create_model(f"{model_type.__name__}Update", **fields)
