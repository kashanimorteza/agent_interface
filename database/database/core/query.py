"""Query (Core): checking Conditions and Sorts against the given Entity."""

import math
from collections.abc import Collection, Iterable
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

from database.core.errors import InvalidInputError
from database.core.values import (
    CheckedFilter,
    CheckedOrder,
    Filter,
    FilterOperator,
    Order,
    OrderDirection,
)

_TEXT_OPERATORS = {
    FilterOperator.CONTAINS,
    FilterOperator.STARTS_WITH,
    FilterOperator.ENDS_WITH,
}
_NULL_OPERATORS = {FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL}
_NUMERIC_TYPES = {"integer", "float", "decimal"}


def field_of(entity: Any, reference: Any) -> tuple[str, str]:
    """Return the name and declared Type of a Field reference of the Entity."""
    declared = {item.name: item.type.value for item in entity.declaration.fields}
    name = getattr(reference, "key", None)
    if (
        isinstance(reference, str)
        or not isinstance(name, str)
        or getattr(reference, "class_", None) is not entity
        or name not in declared
    ):
        raise InvalidInputError(
            f"The Field must be a Field reference of {entity.__name__}"
        )
    return name, declared[name]


def check_identity(entity: Any, value: Any) -> Any:
    """Return an id value in the declared Type of the Entity's id Field."""
    declared = {item.name: item.type.value for item in entity.declaration.fields}
    return _normalized(declared["id"], value, "id")


def numeric_field_of(entity: Any, reference: Any) -> tuple[str, str]:
    name, type_name = field_of(entity, reference)
    if type_name not in _NUMERIC_TYPES:
        raise InvalidInputError(f"The Field {name!r} is not numeric")
    return name, type_name


def _normalized(type_name: str, value: Any, name: str) -> Any:
    """Return value in the Python form of the declared Type, or refuse it."""
    plain_number = isinstance(value, int | float) and not isinstance(value, bool)
    match type_name:
        case "string" if isinstance(value, str):
            return value
        case "integer" if isinstance(value, int) and not isinstance(value, bool):
            return value
        case "float" if plain_number and math.isfinite(value):
            return float(value)
        case "decimal" if isinstance(value, int) and not isinstance(value, bool):
            return Decimal(value)
        case "decimal" if isinstance(value, Decimal) and value.is_finite():
            return value
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
    raise InvalidInputError(f"The value for {name!r} does not match its Type")


def _check_filter(entity: Any, item: Any) -> CheckedFilter:
    if not isinstance(item, Filter):
        raise InvalidInputError("A filter must be a Filter")
    name, type_name = field_of(entity, item.field)
    operator = item.operator
    if operator in _NULL_OPERATORS:
        if item.value is not None:
            raise InvalidInputError(f"The operator {operator.name} takes no value")
        return CheckedFilter(name, type_name, operator, None)
    if item.value is None:
        raise InvalidInputError(f"The operator {operator.name} needs a value")
    if operator in _TEXT_OPERATORS:
        if type_name != "string":
            raise InvalidInputError(
                f"The operator {operator.name} needs a textual Field"
            )
        return CheckedFilter(
            name, type_name, operator, _normalized(type_name, item.value, name)
        )
    if operator is FilterOperator.IN:
        if isinstance(item.value, str | bytes) or not isinstance(
            item.value, Collection
        ):
            raise InvalidInputError("The operator IN needs a collection of values")
        values = tuple(_normalized(type_name, value, name) for value in item.value)
        return CheckedFilter(name, type_name, operator, values)
    return CheckedFilter(
        name, type_name, operator, _normalized(type_name, item.value, name)
    )


def check_filters(
    entity: Any, filters: Iterable[Any] | None
) -> tuple[CheckedFilter, ...]:
    """Check every Filter against the Entity."""
    if filters is None:
        return ()
    if isinstance(filters, Filter | str) or not isinstance(filters, Iterable):
        raise InvalidInputError("The filters must be a sequence of Filters")
    return tuple(_check_filter(entity, item) for item in filters)


def check_orders(entity: Any, orders: Iterable[Any] | None) -> tuple[CheckedOrder, ...]:
    """Check every Order against the Entity."""
    if orders is None:
        return ()
    if isinstance(orders, Order | str) or not isinstance(orders, Iterable):
        raise InvalidInputError("The orders must be a sequence of Orders")
    checked = []
    for item in orders:
        if not isinstance(item, Order):
            raise InvalidInputError("An order must be an Order")
        name, type_name = field_of(entity, item.field)
        checked.append(
            CheckedOrder(name, type_name, item.direction is OrderDirection.DESCENDING)
        )
    return tuple(checked)
