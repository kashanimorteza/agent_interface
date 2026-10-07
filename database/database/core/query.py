from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from database.core.configuration import QueryDefaults
from database.core.errors import ConfigurationError, InvalidInputError
from database.core.tables import field_declaration, normalize_value
from database.core.values import (
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)

_TEXT_OPERATORS = (
    FilterOperator.CONTAINS,
    FilterOperator.STARTS_WITH,
    FilterOperator.ENDS_WITH,
)
_NULL_OPERATORS = (FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL)
_ORDERING_OPERATORS = (
    FilterOperator.GREATER_THAN,
    FilterOperator.GREATER_OR_EQUAL,
    FilterOperator.LESS_THAN,
    FilterOperator.LESS_OR_EQUAL,
)


@dataclass(frozen=True)
class CheckedFilter:
    field: str
    type: str
    operator: FilterOperator
    value: Any


@dataclass(frozen=True)
class CheckedOrder:
    field: str
    type: str
    descending: bool


def check_filter(entity: type[Any], condition: Any) -> CheckedFilter:
    """Check a Filter against its Entity into a checked Filter."""
    if not isinstance(condition, Filter) or not isinstance(condition.operator, FilterOperator):
        raise InvalidInputError("A Filter must be built from a Field reference and an operator.")
    field = field_declaration(entity, condition.field)
    kind = field.type.value
    operator = condition.operator
    label = f"{entity.declaration.name}.{field.name}"
    if operator in _NULL_OPERATORS:
        if condition.value is not None:
            raise InvalidInputError(f"The operator {operator.name} takes no value for {label}.")
        value = None
    elif operator is FilterOperator.IN:
        if not isinstance(condition.value, tuple):
            raise InvalidInputError(f"The operator IN needs a collection of values for {label}.")
        value = tuple(normalize_value(entity, field, item) for item in condition.value)
    elif operator in _TEXT_OPERATORS:
        if kind != "string":
            raise InvalidInputError(f"The operator {operator.name} needs a textual Field: {label}.")
        value = normalize_value(entity, field, condition.value)
    else:
        if kind == "boolean" and operator in _ORDERING_OPERATORS:
            raise InvalidInputError(f"The operator {operator.name} cannot compare {label}.")
        value = normalize_value(entity, field, condition.value)
    return CheckedFilter(field=field.name, type=kind, operator=operator, value=value)


def check_filters(entity: type[Any], filters: Sequence[Filter] | None) -> tuple[CheckedFilter, ...]:
    if filters is None:
        return ()
    if not isinstance(filters, list | tuple):
        raise InvalidInputError("Filters must be given as a list or tuple of Filter values.")
    return tuple(check_filter(entity, condition) for condition in filters)


def check_order(entity: type[Any], order: Any) -> CheckedOrder:
    """Check an Order against its Entity into a checked Order."""
    if not isinstance(order, Order) or not isinstance(order.direction, OrderDirection):
        raise InvalidInputError("An Order must be built from a Field reference and a direction.")
    field = field_declaration(entity, order.field)
    return CheckedOrder(
        field=field.name,
        type=field.type.value,
        descending=order.direction is OrderDirection.DESCENDING,
    )


def resolve_combination(combination: Any, default: FilterCombination) -> FilterCombination:
    if combination is None:
        return default
    if not isinstance(combination, FilterCombination):
        raise InvalidInputError("The combination must be a FilterCombination member.")
    return combination


def resolve_orders(
    entity: type[Any], orders: Sequence[Order] | None, default: QueryDefaults
) -> tuple[CheckedOrder, ...]:
    """Supplied Orders replace the default order and keep their sequence."""
    if orders is None or (isinstance(orders, list | tuple) and not orders):
        field = next((f for f in entity.declaration.fields if f.name == default.order_field), None)
        if field is None:
            raise ConfigurationError(
                f"The default order Field {default.order_field} is not a Field of "
                f"{entity.declaration.name}."
            )
        return (
            CheckedOrder(
                field=field.name,
                type=field.type.value,
                descending=default.order_direction is OrderDirection.DESCENDING,
            ),
        )
    if not isinstance(orders, list | tuple):
        raise InvalidInputError("Orders must be given as a list or tuple of Order values.")
    return tuple(check_order(entity, order) for order in orders)


def resolve_limit(limit: Any, default: QueryDefaults) -> int:
    """A positive limit caps the count; zero or a negative limit means no limit (-1)."""
    if limit is None:
        return default.limit
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise InvalidInputError("The limit must be an integer.")
    return limit if limit > 0 else -1
