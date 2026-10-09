"""The common HTTP rules every Group's Endpoints follow."""

import enum
import inspect
import re
from collections.abc import Callable
from typing import Any

from fastapi import APIRouter
from logic.interface import Entity
from pydantic import BaseModel

METHOD_BY_VERB: dict[str, list[str]] = {
    "GET": ["get", "list", "find", "search", "count", "sum", "min", "max", "read"],
    "PUT": ["update", "replace"],
    "PATCH": ["enable", "disable", "set", "patch"],
    "DELETE": ["delete", "remove", "truncate", "clear"],
}
DEFAULT_METHOD = "POST"

FilterOperator = Entity.database_value.FilterOperator
FilterCombination = Entity.database_value.FilterCombination
OrderDirection = Entity.database_value.OrderDirection

InstanceName = enum.Enum(
    "InstanceName", {member.name: member.name for member in Entity.database_instance}, type=str
)


class FilterForm(BaseModel):
    """The form a Filter travels in: its field name, operator and value."""

    field: str
    operator: FilterOperator
    value: Any = None


class OrderForm(BaseModel):
    """The form an Order travels in: its field name and direction."""

    field: str
    direction: OrderDirection = inspect.signature(Entity.database_value.Order).parameters[
        "direction"
    ].default


def method_of(operation: str) -> str:
    """The Method of an Endpoint: the one its operation's leading verb has in the verb table, else the default."""
    verb = operation.split("_")[0]
    for method, verbs in METHOD_BY_VERB.items():
        if verb in verbs:
            return method
    return DEFAULT_METHOD


def path_of(operation: str, parameters: list[str]) -> str:
    """The Path of an Endpoint: its operation, extended by the id when the operation takes one."""
    return f"/{operation}/{{id}}" if "id" in parameters else f"/{operation}"


def segment(entity: str) -> str:
    """The public segment of an Adapter: its Entity's name in the project's identifier case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", entity).lower()


def actions(child: type) -> dict[str, Callable[..., Any]]:
    """Every Action of a Child Service, in the order its Base publishes them."""
    names: dict[str, None] = {}
    for kind in reversed(child.__mro__):
        for name, member in vars(kind).items():
            if inspect.isfunction(member) and not name.startswith("_"):
                names.setdefault(name)
    return {name: getattr(child, name) for name in names}


class Adapter(APIRouter):
    """The unit of a Group bound permanently to one Child Service and its Entity."""

    def __init__(self, child: type) -> None:
        super().__init__()
        self.entity = getattr(Entity.Model, child.__name__)
        self.service = child()
        for name, action in actions(child).items():
            takes = list(inspect.signature(action).parameters)[1:]
            self.add_api_route(
                path_of(name, takes),
                self.handler(name, action),
                methods=[method_of(name)],
                name=name,
                description=action.__doc__,
            )

    def structure(self, parameter: inspect.Parameter) -> Any:
        """The structure a Parameter has: the Action publishes none, so it follows from the Parameter's name."""
        forms: dict[str, Any] = {
            "entity": self.entity,
            "id": int,
            "field": str,
            "filters": list[FilterForm],
            "orders": list[OrderForm],
            "combination": FilterCombination,
            "limit": int,
            "instance": InstanceName,
        }
        structure = forms.get(parameter.name, parameter.annotation)
        optional = parameter.default is not inspect.Parameter.empty
        return structure | None if optional and parameter.default is None else structure

    def handler(self, name: str, action: Callable[..., Any]) -> Callable[..., Any]:
        """The Handler of one Endpoint: it calls its Action on the bound Child Service."""
        call = getattr(self.service, name)
        published = list(inspect.signature(action).parameters.values())[1:]

        def handle(**arguments: Any) -> Any:
            return call(**arguments)

        handle.__signature__ = inspect.Signature(  # ty: ignore[unresolved-attribute]
            [p.replace(annotation=self.structure(p)) for p in published]
        )
        handle.__name__ = name
        handle.__doc__ = action.__doc__
        return handle
