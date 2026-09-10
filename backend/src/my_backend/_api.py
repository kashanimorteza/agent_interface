from typing import Any, Literal

from fastapi import APIRouter, FastAPI, HTTPException
from my_model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    DomainModel,
    Instance,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from pydantic import BaseModel, create_model

from ._logic import LOGIC_UNITS, ModelLogic

RESOURCE_NAMES: dict[type[DomainModel], str] = {
    User: "users",
    TradingPlatform: "trading-platforms",
    Instance: "instances",
    Currency: "currencies",
    Broker: "brokers",
    Asset: "assets",
    AccountGroup: "account-groups",
    Account: "accounts",
    TrailingGroup: "trailing-groups",
    TrailingRule: "trailing-rules",
    PartialGroup: "partial-groups",
    PartialRule: "partial-rules",
    ActionGroup: "action-groups",
    Action: "actions",
    Position: "positions",
}


def _field_definitions(
    model_cls: type[DomainModel], *, exclude: set[str], force_optional: bool
) -> dict[str, tuple[Any, Any]]:
    defs: dict[str, tuple[Any, Any]] = {}
    for name, info in model_cls.model_fields.items():
        if name in exclude:
            continue
        if force_optional:
            defs[name] = (info.annotation | None, info.default if not info.is_required() else None)
        else:
            defs[name] = (info.annotation, info.default if not info.is_required() else ...)
    return defs


def build_create_schema(model_cls: type[DomainModel]) -> type[BaseModel]:
    defs = _field_definitions(model_cls, exclude={"id"}, force_optional=False)
    return create_model(f"{model_cls.__name__}Create", **defs)


def build_update_schema(model_cls: type[DomainModel]) -> type[BaseModel]:
    defs = _field_definitions(model_cls, exclude={"id"}, force_optional=True)
    return create_model(f"{model_cls.__name__}Update", **defs)


def build_response_schema(model_cls: type[DomainModel]) -> type[BaseModel]:
    defs = _field_definitions(model_cls, exclude=set(model_cls.credential_fields), force_optional=False)
    return create_model(f"{model_cls.__name__}Response", **defs)


def build_router(model_cls: type[DomainModel], logic: ModelLogic, resource_name: str) -> APIRouter:
    router = APIRouter(prefix=f"/{resource_name}", tags=[model_cls.__name__])
    CreateSchema = build_create_schema(model_cls)
    UpdateSchema = build_update_schema(model_cls)
    ResponseSchema = build_response_schema(model_cls)
    has_status = "status" in model_cls.model_fields

    def _to_response(instance: DomainModel) -> BaseModel:
        data = instance.model_dump(exclude=set(model_cls.credential_fields))
        return ResponseSchema(**data)

    @router.post("", response_model=ResponseSchema, status_code=201)
    def create(payload: CreateSchema) -> BaseModel:
        return _to_response(logic.create(payload.model_dump()))

    @router.get("", response_model=list[ResponseSchema])
    def list_all() -> list[BaseModel]:
        return [_to_response(item) for item in logic.list()]

    @router.get("/{item_id}", response_model=ResponseSchema)
    def get(item_id: int) -> BaseModel:
        result = logic.get(item_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"{model_cls.__name__} not found")
        return _to_response(result)

    @router.patch("/{item_id}", response_model=ResponseSchema)
    def update(item_id: int, payload: UpdateSchema) -> BaseModel:
        try:
            return _to_response(logic.update(item_id, payload.model_dump(exclude_unset=True)))
        except LookupError:
            raise HTTPException(status_code=404, detail=f"{model_cls.__name__} not found")

    @router.delete("/{item_id}", status_code=204)
    def delete(item_id: int) -> None:
        if not logic.delete(item_id):
            raise HTTPException(status_code=404, detail=f"{model_cls.__name__} not found")

    if has_status:
        @router.post("/{item_id}/status", response_model=ResponseSchema)
        def set_status(item_id: int, action: Literal["enable", "disable"]) -> BaseModel:
            try:
                return _to_response(logic.set_status(item_id, action))
            except LookupError:
                raise HTTPException(status_code=404, detail=f"{model_cls.__name__} not found")

    return router


app = FastAPI(title="Trading Assistant Backend API")

for _model_cls, _logic_cls in LOGIC_UNITS.items():
    app.include_router(build_router(_model_cls, _logic_cls(), RESOURCE_NAMES[_model_cls]))
