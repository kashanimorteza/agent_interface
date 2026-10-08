"""Query: checking Conditions and Sorts against the Entity they target."""

from collections.abc import Iterable
from datetime import UTC, date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy.orm.attributes import InstrumentedAttribute

from .configuration import QueryDefaults
from .errors import InvalidInputError
from .values import (
    CheckedFilter,
    CheckedOrder,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)

_PYTHON_TYPES: dict[str, type] = {
    "string": str,
    "integer": int,
    "float": float,
    "decimal": Decimal,
    "boolean": bool,
    "datetime": datetime,
    "date": date,
    "time": time,
    "uuid": UUID,
}
_ORDERED = {"string", "integer", "float", "decimal", "datetime", "date", "time"}
_NUMERIC = {"integer", "float", "decimal"}
_TEXT_OPERATORS = {
    FilterOperator.CONTAINS,
    FilterOperator.STARTS_WITH,
    FilterOperator.ENDS_WITH,
}
_COMPARISONS = {
    FilterOperator.GREATER_THAN,
    FilterOperator.GREATER_OR_EQUAL,
    FilterOperator.LESS_THAN,
    FilterOperator.LESS_OR_EQUAL,
}
_NULL_TESTS = {FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL}


def _field_type(entity: Any, reference: Any, where: str) -> tuple[str, str]:
    """Return the name and declared Type of the Field a reference points to, or refuse the reference."""
    if (
        not isinstance(reference, InstrumentedAttribute)
        or reference.class_ is not entity
    ):
        raise InvalidInputError(
            f"{where} must be a Field reference of {entity.__name__}"
        )
    for item in entity.declaration.fields:
        if item.name == reference.key:
            return item.name, str(item.type)
    raise InvalidInputError(f"{where} must be a declared Field of {entity.__name__}")


def compatible(type_name: str, value: Any) -> bool:
    if type(value) is bool:
        return type_name == "boolean"
    if type_name == "datetime":
        return isinstance(value, datetime) and value.utcoffset() is not None
    if type_name == "date":
        return isinstance(value, date) and not isinstance(value, datetime)
    return isinstance(value, _PYTHON_TYPES[type_name])


def _normalized(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone(UTC)
    return value


def check_filter(entity: Any, filter: Any) -> CheckedFilter:
    """Check a Filter against its Entity and return the checked Filter."""
    if not isinstance(filter, Filter):
        raise InvalidInputError("A filter must be a Filter value")
    name, type_name = _field_type(entity, filter.field, "A Filter Field")
    where = f"The Filter on {entity.__name__}.{name}"
    operator = filter.operator
    if not isinstance(operator, FilterOperator):
        raise InvalidInputError(f"{where} must use a FilterOperator member")
    value = filter.value
    if operator in _NULL_TESTS:
        if value is not None:
            raise InvalidInputError(f"{where} takes no value")
        return CheckedFilter(name, type_name, operator, None)
    if value is None:
        raise InvalidInputError(f"{where} needs a value")
    if operator is FilterOperator.IN:
        if not isinstance(value, (list, tuple, set, frozenset)):
            raise InvalidInputError(f"{where} needs a collection of values")
        if not all(compatible(type_name, item) for item in value):
            raise InvalidInputError(
                f"{where} holds a value that does not suit the Field"
            )
        return CheckedFilter(
            name, type_name, operator, tuple(_normalized(item) for item in value)
        )
    if operator in _TEXT_OPERATORS and type_name != "string":
        raise InvalidInputError(f"{where} needs a textual Field")
    if operator in _COMPARISONS and type_name not in _ORDERED:
        raise InvalidInputError(f"{where} needs a Field that can be ordered")
    if not compatible(type_name, value):
        raise InvalidInputError(f"{where} has a value that does not suit the Field")
    return CheckedFilter(name, type_name, operator, _normalized(value))


def check_order(entity: Any, order: Any) -> CheckedOrder:
    """Check an Order against its Entity and return the checked Order."""
    if not isinstance(order, Order):
        raise InvalidInputError("An order must be an Order value")
    name, type_name = _field_type(entity, order.field, "An Order Field")
    if not isinstance(order.direction, OrderDirection):
        raise InvalidInputError(
            f"The Order on {entity.__name__}.{name} must use an OrderDirection member"
        )
    return CheckedOrder(name, type_name, order.direction is OrderDirection.DESCENDING)


def check_aggregate(entity: Any, reference: Any, kind: str) -> tuple[str, str]:
    """Check the Field of a sum, minimum, or maximum and return its name and Type."""
    name, type_name = _field_type(entity, reference, "An aggregate Field")
    allowed = _NUMERIC if kind == "sum" else _ORDERED
    if type_name not in allowed:
        raise InvalidInputError(
            f"The {kind} of {entity.__name__}.{name} needs a {'numeric' if kind == 'sum' else 'comparable'} Field"
        )
    return name, type_name


def check_filters(
    entity: Any, filters: Iterable[Any] | None
) -> tuple[CheckedFilter, ...]:
    """Check every Filter against its Entity."""
    return tuple(check_filter(entity, item) for item in (filters or ()))


def resolve_combination(defaults: QueryDefaults, combination: Any) -> FilterCombination:
    """Return the given Filter combination or the configured default."""
    if combination is None:
        return defaults.combination
    if not isinstance(combination, FilterCombination):
        raise InvalidInputError("A combination must be a FilterCombination member")
    return combination


def resolve_orders(
    entity: Any, defaults: QueryDefaults, orders: Iterable[Any] | None
) -> tuple[CheckedOrder, ...]:
    """Return the checked Orders in the order given, or the configured default order when none is given."""
    given = tuple(orders or ())
    if given:
        return tuple(check_order(entity, item) for item in given)
    for item in entity.declaration.fields:
        if item.name == defaults.order_field:
            return (
                CheckedOrder(
                    item.name,
                    str(item.type),
                    defaults.order_direction is OrderDirection.DESCENDING,
                ),
            )
    raise InvalidInputError(
        f"The default order Field is not a Field of {entity.__name__}"
    )


def resolve_limit(defaults: QueryDefaults, limit: Any) -> int:
    """Return the given limit or the configured default; zero or negative means no limit (-1)."""
    if limit is None:
        return defaults.limit
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise InvalidInputError("A limit must be a whole number")
    return limit if limit > 0 else -1
