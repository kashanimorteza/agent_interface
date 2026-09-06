"""One generic router per shared Model exposing the five standard operations.

Path operations validate the transport shape, invoke the Model's Logic unit, and return the Read schema.
They never call Data Access or the Database package. Plain ``def`` is used because Logic is blocking.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query, Response

from trading_backend.api.dependencies import logic_dependency
from trading_backend.api.schemas import SCHEMAS
from trading_backend.logic.model_logic import ModelLogic
from trading_backend.logic.model_specs import MODEL_KEYS, RESOURCE_NAMES, get_spec

RecordId = Annotated[int, Path(ge=1, description="The record's primary key.")]
Limit = Annotated[int, Query(ge=1, le=500, description="Maximum number of records to return.")]
Offset = Annotated[int, Query(ge=0, description="Number of records to skip.")]
OrderBy = Annotated[
    str | None,
    Query(description="Comma-separated field names to order by; prefix a name with '-' for descending order."),
]


def build_model_router(model: str) -> APIRouter:
    """The router of one Model: POST, GET (list), GET/{id}, PATCH/{id}, DELETE/{id} under /api/<resource>."""
    spec = get_spec(model)
    schemas = SCHEMAS[model]
    Create, Update, Read = schemas.create, schemas.update, schemas.read
    router = APIRouter(prefix=f"/api/{RESOURCE_NAMES[model]}", tags=[model])
    LogicDep = Annotated[ModelLogic, Depends(logic_dependency(model))]

    @router.post("", status_code=201, response_model=Read, operation_id=f"{model}_create", summary=f"Create a {spec.name}")
    def create(body: Create, logic: LogicDep) -> Any:  # type: ignore[valid-type]
        return logic.create(body.model_dump())

    @router.get("", response_model=list[Read], operation_id=f"{model}_list", summary=f"List {spec.name} records")  # type: ignore[valid-type]
    def list_records(logic: LogicDep, limit: Limit = 100, offset: Offset = 0, order_by: OrderBy = None) -> Any:
        fields = [part.strip() for part in order_by.split(",") if part.strip()] if order_by else None
        return logic.list(order_by=fields, limit=limit, offset=offset)

    @router.get("/{record_id}", response_model=Read, operation_id=f"{model}_get", summary=f"Get one {spec.name}")
    def get(record_id: RecordId, logic: LogicDep) -> Any:
        return logic.get(record_id)

    @router.patch("/{record_id}", response_model=Read, operation_id=f"{model}_update", summary=f"Update a {spec.name}")
    def update(record_id: RecordId, body: Update, logic: LogicDep) -> Any:  # type: ignore[valid-type]
        return logic.update(record_id, body.model_dump(exclude_unset=True))

    @router.delete("/{record_id}", status_code=204, response_class=Response, operation_id=f"{model}_delete", summary=f"Delete a {spec.name}")
    def delete(record_id: RecordId, logic: LogicDep) -> Response:
        logic.delete(record_id)
        return Response(status_code=204)

    return router


ROUTERS: list[APIRouter] = [build_model_router(model) for model in MODEL_KEYS]
