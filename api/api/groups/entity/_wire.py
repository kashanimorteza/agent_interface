"""Wire: binds JSON request values to the values Entity Service's Actions take, and encodes results as JSON.

It uses only what Logic's Interface publishes. The Entity of a Child Service is read from the Child Service's own
generic base, so the caller never names an Entity and API imports no other application Component.
"""

import json
import types
import typing
from collections.abc import Callable, Sequence
from datetime import date, datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING, Any, NotRequired, TypedDict
from uuid import UUID

from logic.interface import Entity

if TYPE_CHECKING:
    DatabaseInstance = Any
else:
    DatabaseInstance = Entity.DatabaseInstance


class FilterBody(TypedDict):
    """One condition of a request: a Field name, an operator, and a value."""

    field: str
    operator: Entity.FilterOperator
    value: NotRequired[Any]


class OrderBody(TypedDict):
    """One ordering of a request: a Field name and an optional direction."""

    field: str
    direction: NotRequired[Entity.OrderDirection]


_PARSERS: dict[str, Callable[[Any], Any]] = {
    "decimal": lambda value: Decimal(str(value)),
    "datetime": datetime.fromisoformat,
    "date": date.fromisoformat,
    "time": time.fromisoformat,
    "uuid": UUID,
}


def entity_of(service: type) -> Any:
    """The Entity a Child Service is bound to, read from its generic base."""
    return typing.get_args(types.get_original_bases(service)[0])[0]


def bind_entity(service: type, entity: dict[str, Any]) -> Any:
    """The Entity whose JSON text the request content is."""
    return entity_of(service).from_json(json.dumps(entity))


def bind_field(service: type, name: str) -> Any:
    """The Entity's Field reference for a Field name; anything else reaches the Action as given."""
    return getattr(entity_of(service), name, None)


def _bind_value(service: type, name: str, value: Any) -> Any:
    """A condition value in the Python type its Field has in the Entity."""
    declared = {
        field.name: field.type for field in entity_of(service).declaration.fields
    }
    parse = _PARSERS.get(declared.get(name, ""))
    if parse is None or value is None:
        return value
    if isinstance(value, list):
        return [parse(item) for item in value]
    return parse(value)


def bind_filters(
    service: type, filters: Sequence[FilterBody] | None
) -> list[Entity.Filter] | None:
    """The Filters a request expresses, or none when it expresses none."""
    if filters is None:
        return None
    return [
        Entity.Filter(
            bind_field(service, item["field"]),
            item["operator"],
            _bind_value(service, item["field"], item.get("value")),
        )
        for item in filters
    ]


def bind_orders(
    service: type, orders: Sequence[OrderBody] | None
) -> list[Entity.Order] | None:
    """The Orders a request expresses, or none when it expresses none."""
    if orders is None:
        return None
    return [
        Entity.Order(bind_field(service, item["field"]), item["direction"])
        if "direction" in item
        else Entity.Order(bind_field(service, item["field"]))
        for item in orders
    ]


def encode(result: Any) -> Any:
    """An Action's result as JSON content: an Entity as its JSON object, exact values as the Model writes them."""
    if isinstance(result, Decimal):
        return format(result, "f")
    if isinstance(result, datetime | date | time):
        return result.isoformat()
    if isinstance(result, UUID):
        return str(result)
    if isinstance(result, list | tuple):
        return [encode(item) for item in result]
    if hasattr(result, "to_json"):
        return json.loads(result.to_json())
    return result
