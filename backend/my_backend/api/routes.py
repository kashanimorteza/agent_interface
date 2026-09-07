"""The standard Model operations, one router per shared Model.

Each operation decodes the request into the representation derived from the
Model, invokes the Model's Logic unit through the registry, and serializes the
result into the output representation, which carries no credential.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Path
from my_model import Model
from pydantic import BaseModel

from ..logic import LogicRegistry
from .schemas import input_schema, output_schema, resource_name

Key = Annotated[int, Path(ge=1, description="The record identifier")]


def router_for(model: type[Model], registry: LogicRegistry) -> APIRouter:
    Create = input_schema(model)
    Update = input_schema(model, partial=True)
    Out = output_schema(model)
    resource = resource_name(model)
    router = APIRouter(prefix=f"/{resource}", tags=[model.logical_name])

    def unit():
        return registry.for_model(model)

    def out(value: Model) -> BaseModel:
        return Out.model_validate(value.model_dump())

    @router.post("", status_code=201, response_model=Out, operation_id=f"create_{resource}",
                 summary=f"Create a {model.logical_name}")
    def create(payload: Create) -> Any:  # type: ignore[valid-type]
        return out(unit().create(payload.model_dump()))

    @router.get("", response_model=list[Out], operation_id=f"list_{resource}",
                summary=f"List every {model.logical_name}")
    def list_all() -> Any:
        return [out(value) for value in unit().list()]

    @router.get("/{key}", response_model=Out, operation_id=f"get_{resource}",
                summary=f"Get one {model.logical_name}")
    def get(key: Key) -> Any:
        return out(unit().get(key))

    @router.patch("/{key}", response_model=Out, operation_id=f"update_{resource}",
                  summary=f"Update a {model.logical_name}")
    def update(key: Key, payload: Update) -> Any:  # type: ignore[valid-type]
        return out(unit().update(key, payload.model_dump(exclude_unset=True)))

    @router.delete("/{key}", status_code=204, operation_id=f"delete_{resource}",
                   summary=f"Delete a {model.logical_name}")
    def delete(key: Key) -> None:
        unit().delete(key)

    return router
