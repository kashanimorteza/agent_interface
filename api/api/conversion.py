"""Conversion of non-simple Parameters between their transport forms and the types the Logic Interface publishes."""

import json
from collections.abc import Callable
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import Annotated, Any
from uuid import UUID

from logic.interface import Entity
from pydantic import AfterValidator, BaseModel, ConfigDict

database_error = Entity.database_error
database_instance = Entity.database_instance
database_value = Entity.database_value

_DECODERS: dict[str, Callable[[str], Any]] = {
    "decimal": Decimal,
    "datetime": datetime.fromisoformat,
    "date": date.fromisoformat,
    "time": time.fromisoformat,
    "uuid": UUID,
}


class FilterBody(BaseModel):
    """The transport form of a Filter."""

    model_config = ConfigDict(extra="forbid")

    field: str
    operator: str
    value: Any = None


class OrderBody(BaseModel):
    """The transport form of an Order."""

    model_config = ConfigDict(extra="forbid")

    field: str
    direction: str = "ASCENDING"


FilterList = list[FilterBody]
OrderList = list[OrderBody]


def _refuse(message: str) -> Exception:
    return database_error.InvalidInputError(message)


def _member(group: Any, name: str, kind: str) -> Any:
    try:
        return group[name]
    except KeyError:
        raise _refuse(f"'{name}' is not a known {kind}") from None


def _field(entity: Any, name: str) -> Any:
    if name not in entity.model_fields:
        raise _refuse(f"'{name}' is not a Field of {entity.__name__}")
    return getattr(entity, name)


def _decoded(entity: Any, name: str, raw: Any) -> Any:
    kind = next(f.type.name for f in entity.declaration.fields if f.name == name)
    decode = _DECODERS.get(kind)
    if decode is None:
        return raw
    try:
        if isinstance(raw, list):
            return [decode(i) if isinstance(i, str) else i for i in raw]
        return decode(raw) if isinstance(raw, str) else raw
    except ValueError, TypeError, InvalidOperation:
        raise _refuse(f"The value of '{name}' is not a valid {kind}") from None


def to_instance(name: str | None) -> Any:
    """Convert an Instance name into the published Instance."""
    if name is None:
        return None
    return _member(database_instance.__members__, name, "Instance")


def to_combination(name: str | None) -> Any:
    """Convert a combination name into the published FilterCombination."""
    if name is None:
        return None
    return _member(database_value.FilterCombination, name, "combination")


Instance = Annotated[str | None, AfterValidator(to_instance)]
Combination = Annotated[str | None, AfterValidator(to_combination)]


def to_field(entity: Any) -> Callable[[str], Any]:
    """Return the conversion of a Field name into the Field of the bound Entity."""

    def convert(name: str) -> Any:
        return _field(entity, name)

    return convert


def to_filters(entity: Any) -> Callable[[FilterList | None], Any]:
    """Return the conversion of Filter objects into published Filters of the bound Entity."""

    def convert(items: FilterList | None) -> Any:
        if items is None:
            return None
        return [
            database_value.Filter(
                _field(entity, item.field),
                _member(database_value.FilterOperator, item.operator, "operator"),
                _decoded(entity, item.field, item.value),
            )
            for item in items
        ]

    return convert


def to_orders(entity: Any) -> Callable[[OrderList | None], Any]:
    """Return the conversion of Order objects into published Orders of the bound Entity."""

    def convert(items: OrderList | None) -> Any:
        if items is None:
            return None
        return [
            database_value.Order(
                _field(entity, item.field),
                _member(database_value.OrderDirection, item.direction, "direction"),
            )
            for item in items
        ]

    return convert


def to_entity(entity: Any) -> Callable[[dict[str, Any]], Any]:
    """Return the conversion of a JSON object of Fields into an instance of the bound Entity."""
    generated = [
        f.name
        for f in entity.declaration.fields
        if f.value_generation is not None
        and f.value_generation.value == "auto_increment"
    ]

    def convert(data: dict[str, Any]) -> Any:
        values = dict(data)
        stored = {n: values.pop(n) for n in generated if values.get(n) is not None}
        for name in generated:
            values.pop(name, None)
        for name, value in stored.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise _refuse(f"The identity '{name}' must be an integer")
        try:
            built = entity.from_json(json.dumps(values))
        except (ValueError, TypeError) as error:
            raise _refuse(str(error)) from None
        if not stored:
            return built
        kept = {n: getattr(built, n) for n in entity.model_fields if n not in generated}
        return entity.model_construct(**kept, **stored)

    return convert
