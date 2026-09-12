"""Shared, parameterized router construction reused by every Model's own API router.

Each Model still gets its own router (its own module, its own registered
path prefix and schemas); this factory only removes boilerplate duplicated
across all fifteen otherwise-identical routers. Routers are thin: they
decode input, call the corresponding Logic unit, and map results — they
never call Model Interface, Database Interface, Model, or Database directly.
"""

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel as PydanticBaseModel

from my_backend import _database_interface as db
from my_backend.logic._base import ModelLogic


def build_router(
    *,
    name: str,
    logic_cls: type[ModelLogic],
    read_schema: type[PydanticBaseModel],
    create_schema: type[PydanticBaseModel],
    update_schema: type[PydanticBaseModel],
    prefix: str,
    has_status: bool,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[name])
    slug = name.lower()

    @router.post(
        "",
        response_model=read_schema,
        status_code=201,
        operation_id=f"{slug}_create",
        summary=f"Create a {name}",
    )
    def create_record(payload: create_schema):  # type: ignore[valid-type]
        data = payload.model_dump()
        try:
            return logic_cls.create(data)
        except db.ConstraintViolationError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.get(
        "/{record_id}",
        response_model=read_schema,
        operation_id=f"{slug}_get",
        summary=f"Get a {name} by id",
    )
    def get_record(record_id: int):
        record = logic_cls.get(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail=f"{name} {record_id} not found")
        return record

    @router.get(
        "",
        response_model=list[read_schema],
        operation_id=f"{slug}_list",
        summary=f"List {name} records",
    )
    def list_records(limit: int | None = None, offset: int | None = None):
        return logic_cls.list(limit=limit, offset=offset)

    @router.patch(
        "/{record_id}",
        response_model=read_schema,
        operation_id=f"{slug}_update",
        summary=f"Update a {name}",
    )
    def update_record(record_id: int, payload: update_schema):  # type: ignore[valid-type]
        changes = payload.model_dump(exclude_unset=True)
        try:
            return logic_cls.update(record_id, changes)
        except db.NotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except db.ConstraintViolationError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.delete(
        "/{record_id}",
        status_code=204,
        operation_id=f"{slug}_delete",
        summary=f"Delete a {name}",
    )
    def delete_record(record_id: int):
        deleted = logic_cls.delete(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"{name} {record_id} not found")

    if has_status:

        @router.post(
            "/{record_id}/status",
            response_model=read_schema,
            operation_id=f"{slug}_set_status",
            summary=f"Enable or disable a {name}",
        )
        def set_status_record(record_id: int, action: Literal["enable", "disable"]):
            try:
                return logic_cls.set_status(record_id, action)
            except db.NotFoundError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc
            except db.UnsupportedOperationError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

    return router
