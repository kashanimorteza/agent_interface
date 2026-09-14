"""Generic router construction for one Model Logic unit (task P3-G10-T1).

Deliberately does not use `from __future__ import annotations`: each route function
below annotates its body parameter with a dynamically generated Pydantic schema bound
in this function's closure, and FastAPI resolves parameter annotations by inspecting the
live function object. A string (postponed) annotation would only be resolvable against
the module's globals, not this closure, and would fail to bind at runtime.

Every closure-local annotation below (the per-Model schema variables, `LogicDep`,
`PaginationDep`) is a real, valid runtime type — FastAPI resolves and validates against
it on every request — but pyright only recognizes a function-local variable as a type
alias when it is a module- or class-level binding, so it misreports each one here.
"""

# pyright: reportInvalidTypeForm=false

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, status

from ..logic.auth import authorize
from ..logic.registry import ModelLogicBase
from .deps import AuthenticatedContextDep, DatabaseInterfaceDep
from .pagination import PaginationParams, apply_pagination, get_pagination
from .schemas import create_schema_for, output_schema_for, update_schema_for


def build_router(logic_cls: type[ModelLogicBase[Any]], *, prefix: str) -> APIRouter:
    model_cls = logic_cls.model_cls
    model_name = model_cls.__name__
    create_schema = create_schema_for(model_cls)
    update_schema = update_schema_for(model_cls)
    output_schema = output_schema_for(model_cls)

    router = APIRouter(prefix=prefix, tags=[model_name])

    def get_logic(db: DatabaseInterfaceDep) -> ModelLogicBase[Any]:
        return logic_cls(db)

    LogicDep = Annotated[ModelLogicBase[Any], Depends(get_logic)]
    PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]

    @router.post("", response_model=output_schema, status_code=status.HTTP_201_CREATED)
    def create(payload: create_schema, logic: LogicDep, ctx: AuthenticatedContextDep) -> Any:
        authorize(ctx, operation=f"create_{model_name}")
        return logic.create(payload.model_dump())

    @router.get("/search", response_model=list[output_schema])
    def search(
        request: Request,
        logic: LogicDep,
        ctx: AuthenticatedContextDep,
        pagination: PaginationDep,
    ) -> Any:
        authorize(ctx, operation=f"search_{model_name}")
        filters = {
            key: value
            for key, value in request.query_params.items()
            if key not in {"cursor", "limit"}
        }
        unknown = sorted(set(filters) - set(model_cls.model_fields))
        if unknown:
            from ..logic.outcomes import ValidationFailed

            raise ValidationFailed(f"Unknown search fields: {', '.join(unknown)}")
        return apply_pagination(logic.search(**filters), pagination)

    @router.get("/{item_id}", response_model=output_schema)
    def get_by_id(item_id: int, logic: LogicDep, ctx: AuthenticatedContextDep) -> Any:
        authorize(ctx, operation=f"get_{model_name}")
        return logic.get_by_id(item_id)

    @router.get("", response_model=list[output_schema])
    def list_items(logic: LogicDep, ctx: AuthenticatedContextDep, pagination: PaginationDep) -> Any:
        authorize(ctx, operation=f"list_{model_name}")
        return apply_pagination(logic.list(), pagination)

    @router.put("/{item_id}", response_model=output_schema)
    def update(
        item_id: int, payload: update_schema, logic: LogicDep, ctx: AuthenticatedContextDep
    ) -> Any:
        authorize(ctx, operation=f"update_{model_name}")
        data = payload.model_dump(exclude_unset=True)
        return logic.update(item_id, data)

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(item_id: int, logic: LogicDep, ctx: AuthenticatedContextDep) -> None:
        authorize(ctx, operation=f"delete_{model_name}")
        logic.delete(item_id)

    if "is_active" in model_cls.model_fields:

        @router.post("/{item_id}/enable", response_model=output_schema)
        def enable(item_id: int, logic: LogicDep, ctx: AuthenticatedContextDep) -> Any:
            authorize(ctx, operation=f"enable_{model_name}")
            return logic.enable(item_id)

        @router.post("/{item_id}/disable", response_model=output_schema)
        def disable(item_id: int, logic: LogicDep, ctx: AuthenticatedContextDep) -> Any:
            authorize(ctx, operation=f"disable_{model_name}")
            return logic.disable(item_id)

    return router
