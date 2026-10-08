"""Checking of Entities, Fields, Conditions and Sorts against the Entity a request names."""

import math
from collections.abc import Sequence
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

from model.interface import entities
from sqlalchemy.orm.attributes import InstrumentedAttribute

from database.core.errors import InvalidInputError
from database.core.values import (
    CheckedFilter,
    CheckedOrder,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)

_COMPARABLE = ("string", "integer", "float", "decimal", "datetime", "date", "time")
_NUMERIC = ("integer", "float", "decimal")
_TEXT = (FilterOperator.CONTAINS, FilterOperator.STARTS_WITH, FilterOperator.ENDS_WITH)
_NULL = (FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL)


def check_entity(entity: Any) -> type:
    """Return the Entity class of an Entity class or Entity instance from the Model Entity Collection."""
    cls = entity if isinstance(entity, type) else type(entity)
    if cls not in entities:
        raise InvalidInputError(
            "A request names an Entity of the Model Entity Collection."
        )
    return cls


def check_entity_class(entity: Any) -> type:
    """Return an Entity class; an Entity instance or any other value is refused."""
    if not isinstance(entity, type):
        raise InvalidInputError("This request takes an Entity class.")
    return check_entity(entity)


def check_entity_instance(entity: Any) -> Any:
    """Return an Entity instance; an Entity class or any other value is refused."""
    if isinstance(entity, type):
        raise InvalidInputError("This request takes an Entity instance.")
    check_entity(entity)
    return entity


def check_id(value: Any) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise InvalidInputError("An id is an integer.")
    return value


def check_field(entity: type, reference: Any) -> tuple[str, str]:
    """Return the name and declared Type of a Field reference the Entity exposes."""
    if (
        not isinstance(reference, InstrumentedAttribute)
        or reference.class_ is not entity
    ):
        raise InvalidInputError("A Field is given as a Field reference of the Entity.")
    for field in entity.declaration.fields:
        if field.name == reference.key:
            return field.name, field.type.value
    raise InvalidInputError("A Field is given as a Field reference of the Entity.")


def normalize_value(field_type: str, value: Any) -> Any:
    """Return a value compatible with a declared Type, or refuse it without coercing across Types."""
    plain_int = isinstance(value, int) and not isinstance(value, bool)
    match field_type:
        case "string" if isinstance(value, str):
            return value
        case "integer" if plain_int:
            return value
        case "float" if plain_int or (
            isinstance(value, float) and math.isfinite(value)
        ):
            return float(value)
        case "decimal" if plain_int or (
            isinstance(value, Decimal) and value.is_finite()
        ):
            return Decimal(value)
        case "boolean" if isinstance(value, bool):
            return value
        case "datetime" if (
            isinstance(value, datetime) and value.utcoffset() is not None
        ):
            return value
        case "date" if isinstance(value, date) and not isinstance(value, datetime):
            return value
        case "time" if isinstance(value, time):
            return value
        case "uuid" if isinstance(value, UUID):
            return value
    raise InvalidInputError("A value is not compatible with the Field it is used with.")


def _check_filter(entity: type, item: Any) -> CheckedFilter:
    if not isinstance(item, Filter) or not isinstance(item.operator, FilterOperator):
        raise InvalidInputError(
            "A Filter is built from the Filter value with a FilterOperator member."
        )
    name, field_type = check_field(entity, item.field)
    operator, value = item.operator, item.value
    if operator in _NULL:
        if value is not None:
            raise InvalidInputError("This operator takes no value.")
        return CheckedFilter(name, field_type, operator, None)
    if value is None:
        raise InvalidInputError("This operator needs a value.")
    if operator in _TEXT:
        if field_type != "string" or not isinstance(value, str):
            raise InvalidInputError(
                "A text operator needs a textual Field and a text value."
            )
        return CheckedFilter(name, field_type, operator, value)
    if operator is FilterOperator.IN:
        if not isinstance(value, list | tuple | set | frozenset) or not value:
            raise InvalidInputError("IN needs a non-empty collection of values.")
        return CheckedFilter(
            name,
            field_type,
            operator,
            tuple(normalize_value(field_type, v) for v in value),
        )
    return CheckedFilter(name, field_type, operator, normalize_value(field_type, value))


def check_filters(entity: type, filters: Any) -> tuple[CheckedFilter, ...]:
    if filters is None:
        return ()
    if not isinstance(filters, Sequence) or isinstance(filters, str | bytes):
        raise InvalidInputError("Filters are given as a sequence of Filter values.")
    return tuple(_check_filter(entity, item) for item in filters)


def check_combination(
    combination: Any, default: FilterCombination
) -> FilterCombination:
    if combination is None:
        return default
    if not isinstance(combination, FilterCombination):
        raise InvalidInputError("A combination is a FilterCombination member.")
    return combination


def check_orders(
    entity: type, orders: Any, default_field: str, default_direction: OrderDirection
) -> tuple[CheckedOrder, ...]:
    if orders is None:
        reference = getattr(entity, default_field, None)
        name, field_type = check_field(entity, reference)
        return (
            CheckedOrder(
                name, field_type, default_direction is OrderDirection.DESCENDING
            ),
        )
    if not isinstance(orders, Sequence) or isinstance(orders, str | bytes):
        raise InvalidInputError("Orders are given as a sequence of Order values.")
    checked = []
    for item in orders:
        if not isinstance(item, Order) or not isinstance(
            item.direction, OrderDirection
        ):
            raise InvalidInputError(
                "An Order is built from the Order value with an OrderDirection member."
            )
        name, field_type = check_field(entity, item.field)
        checked.append(
            CheckedOrder(name, field_type, item.direction is OrderDirection.DESCENDING)
        )
    return tuple(checked)


def check_limit(limit: Any, default: int) -> int:
    if limit is None:
        return default
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise InvalidInputError("A limit is an integer.")
    return limit if limit > 0 else -1


def check_aggregate_field(
    entity: type, reference: Any, operation: str
) -> tuple[str, str]:
    name, field_type = check_field(entity, reference)
    allowed = _NUMERIC if operation == "sum" else _COMPARABLE
    if field_type not in allowed:
        raise InvalidInputError(
            f"{operation} needs a {'numeric' if operation == 'sum' else 'comparable'} Field."
        )
    return name, field_type
