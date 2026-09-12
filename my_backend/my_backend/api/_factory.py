"""Builds one API Interface router per Model Logic unit.

Deliberately does NOT use `from __future__ import annotations`: each router
is parameterized by dynamically built schema types, and FastAPI must
resolve their real annotations at runtime to validate and document them.
"""

from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from my_backend import _model_interface
from my_backend._schemas import build_schemas
from my_backend.logic._base import ModelLogic


def _to_read(record: _model_interface.BaseModel, read_schema: type[BaseModel]) -> dict[str, Any]:
    # Returns a plain dict rather than a `read_schema` instance: the route's
    # `response_model=read_schema` already validates and serializes this
    # value, so constructing a `read_schema` instance here as well would
    # validate the same data twice for every response.
    values = record.model_dump()
    return {name: values[name] for name in read_schema.model_fields}


def build_router(logic: ModelLogic, *, prefix: str, tag: str) -> APIRouter:
    # Every Model type reaches this layer only through the Model Logic unit
    # that owns it, never through a direct Model import.
    model_type = logic.model_type
    # read_schema already excludes every Credential field (see build_schemas);
    # every response in this router is constructed through it exclusively.
    create_schema, update_schema, read_schema = build_schemas(model_type)
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.post("", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create(payload: create_schema) -> dict[str, Any]:  # type: ignore[valid-type]
        record = logic.create(payload.model_dump())
        return _to_read(record, read_schema)

    @router.get("/{id}", response_model=read_schema)
    def get(id: int) -> dict[str, Any]:
        record = logic.get(id)
        return _to_read(record, read_schema)

    @router.get("", response_model=list[read_schema])
    def list_(limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        records = logic.list(limit=limit, offset=offset)
        return [_to_read(record, read_schema) for record in records]

    @router.patch("/{id}", response_model=read_schema)
    def update(id: int, payload: update_schema) -> dict[str, Any]:  # type: ignore[valid-type]
        # exclude_unset preserves the distinction between an omitted field
        # (left unchanged) and an explicitly supplied field (including null,
        # where the Model permits it), matching partial-update semantics.
        patch = payload.model_dump(exclude_unset=True)
        record = logic.update(id, patch)
        return _to_read(record, read_schema)

    @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(id: int) -> None:
        logic.delete(id)

    if "status" in model_type.model_fields:

        class StatusAction(BaseModel):
            action: str

        @router.post("/{id}/status", response_model=read_schema)
        def set_status(id: int, payload: StatusAction) -> dict[str, Any]:
            record = logic.set_status(id, payload.action)  # type: ignore[arg-type]
            return _to_read(record, read_schema)

    return router
