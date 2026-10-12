"""Checking Conditions and Sorts against the given Entity."""

import datetime
import decimal
import math
import uuid
from collections.abc import Callable
from typing import Any

from model.interface import entities

from database.core.configuration import QueryDefaults
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

_TEXTUAL = frozenset({"string"})
_NUMERIC = frozenset({"integer", "float", "decimal"})
_COMPARABLE = _NUMERIC | {"string", "datetime", "date", "time"}
_TEXT_OPERATORS = frozenset(
    {FilterOperator.CONTAINS, FilterOperator.STARTS_WITH, FilterOperator.ENDS_WITH}
)
_NULL_OPERATORS = frozenset({FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL})
_COLLECTIONS = (list, tuple, set, frozenset)


def _aware(value: Any) -> bool:
    return isinstance(value, datetime.datetime) and value.utcoffset() is not None


_CONFORMS: dict[str, Callable[[Any], bool]] = {
    "string": lambda value: isinstance(value, str),
    "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
    "float": lambda value: (
        isinstance(value, int | float)
        and not isinstance(value, bool)
        and math.isfinite(value)
    ),
    "decimal": lambda value: isinstance(value, decimal.Decimal) and value.is_finite(),
    "boolean": lambda value: isinstance(value, bool),
    "datetime": _aware,
    "date": lambda value: (
        isinstance(value, datetime.date) and not isinstance(value, datetime.datetime)
    ),
    "time": lambda value: isinstance(value, datetime.time),
    "uuid": lambda value: isinstance(value, uuid.UUID),
}


def _normalized(value: Any) -> Any:
    if isinstance(value, datetime.datetime):
        return value.astimezone(datetime.UTC)
    return value


def check_entity(entity: Any) -> Any:
    """The Entity class itself, refusing anything outside the Model Entity Collection."""
    if not any(entity is member for member in entities):
        raise InvalidInputError("entity must be an Entity class of the Model Interface")
    return entity


def check_instance_of(entity: Any) -> Any:
    """The Entity class of an Entity instance, refusing anything else."""
    kind = type(entity)
    if not any(kind is member for member in entities):
        raise InvalidInputError("entity must be an instance of a Model Entity")
    return kind


def field_type(entity: Any, name: str) -> str:
    """The declared Type of one Field of the Entity."""
    for declared in entity.declaration.fields:
        if declared.name == name:
            return str(declared.type.value)
    raise InvalidInputError(f"{entity.__name__} has no Field {name!r}")


def check_field(entity: Any, reference: Any, purpose: str) -> tuple[str, str]:
    """The name and declared Type of a Field reference the Entity exposes."""
    name = getattr(reference, "key", None)
    if (
        not isinstance(name, str)
        or getattr(reference, "class_", None) is not entity
        or getattr(entity, name, None) is not reference
    ):
        raise InvalidInputError(
            f"{purpose} must be a Field reference of {entity.__name__}"
        )
    return name, field_type(entity, name)


def _check_filter(entity: Any, condition: Any) -> CheckedFilter:
    if not isinstance(condition, Filter):
        raise InvalidInputError("every filter must be a Filter")
    name, kind = check_field(entity, condition.field, "a Filter field")
    operator, value = condition.operator, condition.value
    where = f"Filter on {entity.__name__}.{name}"
    if not isinstance(operator, FilterOperator):
        raise InvalidInputError(f"{where} needs a FilterOperator member")
    if operator in _NULL_OPERATORS:
        if value is not None:
            raise InvalidInputError(f"{where} takes no value for {operator.name}")
        return CheckedFilter(field=name, type=kind, operator=operator, value=None)
    if operator in _TEXT_OPERATORS and kind not in _TEXTUAL:
        raise InvalidInputError(f"{where} needs a textual Field for {operator.name}")
    if operator is FilterOperator.IN:
        if not isinstance(value, _COLLECTIONS) or not all(
            _CONFORMS[kind](item) for item in value
        ):
            raise InvalidInputError(
                f"{where} needs a collection of {kind} values for IN"
            )
        return CheckedFilter(
            field=name,
            type=kind,
            operator=operator,
            value=tuple(_normalized(item) for item in value),
        )
    if not _CONFORMS[kind](value):
        raise InvalidInputError(f"{where} needs a {kind} value for {operator.name}")
    return CheckedFilter(
        field=name, type=kind, operator=operator, value=_normalized(value)
    )


def check_filters(
    entity: Any, filters: Any, combination: Any, defaults: QueryDefaults
) -> tuple[tuple[CheckedFilter, ...], FilterCombination]:
    """Checked Filters and the resolved FilterCombination."""
    if filters is None:
        filters = ()
    if not isinstance(filters, list | tuple):
        raise InvalidInputError("filters must be a list of Filter values")
    if combination is None:
        combination = defaults.combination
    if not isinstance(combination, FilterCombination):
        raise InvalidInputError("combination must be a FilterCombination member")
    return tuple(_check_filter(entity, item) for item in filters), combination


def check_orders(
    entity: Any, orders: Any, defaults: QueryDefaults
) -> tuple[CheckedOrder, ...]:
    """Checked Orders in supplied order, or the default Order when none is supplied."""
    if orders is None or (isinstance(orders, list | tuple) and not orders):
        name = defaults.order_field
        return (
            CheckedOrder(
                field=name,
                type=field_type(entity, name),
                descending=defaults.order_direction is OrderDirection.DESCENDING,
            ),
        )
    if not isinstance(orders, list | tuple):
        raise InvalidInputError("orders must be a list of Order values")
    checked: list[CheckedOrder] = []
    for order in orders:
        if not isinstance(order, Order):
            raise InvalidInputError("every order must be an Order")
        name, kind = check_field(entity, order.field, "an Order field")
        if not isinstance(order.direction, OrderDirection):
            raise InvalidInputError(
                f"Order on {entity.__name__}.{name} needs an OrderDirection member"
            )
        checked.append(
            CheckedOrder(
                field=name,
                type=kind,
                descending=order.direction is OrderDirection.DESCENDING,
            )
        )
    return tuple(checked)


def check_limit(limit: Any, defaults: QueryDefaults) -> int:
    """The resolved limit: a positive maximum count, or -1 for no limit."""
    if limit is None:
        return defaults.limit
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise InvalidInputError("limit must be an integer")
    return limit if limit > 0 else -1


def check_aggregate_field(
    entity: Any, reference: Any, numeric: bool
) -> tuple[str, str]:
    """The name and declared Type of an aggregate Field."""
    name, kind = check_field(entity, reference, "the aggregate field")
    allowed = _NUMERIC if numeric else _COMPARABLE
    if kind not in allowed:
        need = "numeric" if numeric else "comparable"
        raise InvalidInputError(f"{entity.__name__}.{name} is not a {need} Field")
    return name, kind
