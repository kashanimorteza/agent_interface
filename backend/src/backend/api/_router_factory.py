"""Builds one API router exposing the standard operations for one Model.

Generic across every Model, so the API layer needs no per-Model endpoint
code; a Model's Logic unit is still separately defined (see ``logic``), and
this factory only wires the transport boundary in front of it.
"""

from typing import Annotated, Literal

import my_model as m
from fastapi import APIRouter, Query, Response
from pydantic import BaseModel

from .. import data_access
from ..logic import ModelLogic
from ._errors import to_http
from ._schemas import create_schema, read_schema, update_schema


class StatusAction(BaseModel):
    action: Literal["enable", "disable"]


def build_router(
    model_type: type[m.BaseModel], logic: ModelLogic, resource: str, tag: str
) -> APIRouter:
    router = APIRouter(prefix=f"/{resource}", tags=[tag])

    Read = read_schema(model_type)
    Create = create_schema(model_type)
    Update = update_schema(model_type)

    @router.post("", response_model=Read, status_code=201, name=f"create_{resource}")
    def create(payload: Create) -> m.BaseModel:  # type: ignore[valid-type]
        try:
            return logic.create(**payload.model_dump())
        except data_access.DatabaseError as error:
            raise to_http(error) from error

    @router.get("/{id}", response_model=Read, name=f"get_{resource}")
    def get(id: int) -> m.BaseModel:
        try:
            return logic.get(id)
        except data_access.DatabaseError as error:
            raise to_http(error) from error

    @router.get("", response_model=list[Read], name=f"list_{resource}")
    def list_(
        limit: Annotated[int | None, Query(ge=1, le=500)] = None,
        offset: Annotated[int, Query(ge=0)] = 0,
    ) -> list[m.BaseModel]:
        try:
            return logic.list(limit=limit, offset=offset)
        except data_access.DatabaseError as error:
            raise to_http(error) from error

    @router.patch("/{id}", response_model=Read, name=f"update_{resource}")
    def update(id: int, payload: Update) -> m.BaseModel:  # type: ignore[valid-type]
        try:
            return logic.update(id, **payload.model_dump(exclude_unset=True))
        except data_access.DatabaseError as error:
            raise to_http(error) from error

    @router.delete("/{id}", status_code=204, name=f"delete_{resource}")
    def delete(id: int) -> Response:
        try:
            logic.delete(id)
        except data_access.DatabaseError as error:
            raise to_http(error) from error
        return Response(status_code=204)

    @router.post("/{id}/status", response_model=Read, name=f"set_status_{resource}")
    def set_status(id: int, payload: StatusAction) -> m.BaseModel:
        try:
            return logic.set_status(id, payload.action)
        except data_access.DatabaseError as error:
            raise to_http(error) from error

    return router
