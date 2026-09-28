"""Interface: the only public Database layer.

Publishes the request vocabulary and the Database Operations. Every Operation
receives an Entity class or Entity instance directly and accepts an optional
Instance; when omitted, the configured default Instance is used.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from sqlmodel import SQLModel

from database import data

__all__ = [
    "CommandResult",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "Order",
    "OrderDirection",
    "add",
    "count",
    "delete",
    "disable",
    "enable",
    "execute_command",
    "get_by_id",
    "list_",
    "max_",
    "min_",
    "sum_",
    "truncate",
    "update",
]


class FilterOperator(StrEnum):
    """One supported comparison for a Filter."""

    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    GREATER_OR_EQUAL = "greater_or_equal"
    LESS_THAN = "less_than"
    LESS_OR_EQUAL = "less_or_equal"
    IN = "in"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


class FilterCombination(StrEnum):
    """How List combines its Filters."""

    AND = "AND"
    OR = "OR"


class OrderDirection(StrEnum):
    """The direction of one Order."""

    ASCENDING = "ascending"
    DESCENDING = "descending"


@dataclass(frozen=True, slots=True)
class Filter:
    """One condition: an Entity Field, a Filter Operator, and a value."""

    field: str
    operator: FilterOperator
    value: Any = None


@dataclass(frozen=True, slots=True)
class Order:
    """One ordering instruction: an Entity Field and an Order Direction."""

    field: str
    direction: OrderDirection = OrderDirection.ASCENDING


@dataclass(frozen=True, slots=True)
class CommandResult:
    """The standard result of Execute Command; a value that does not apply is None."""

    rows: list[dict[str, Any]] | None = None
    affected_count: int | None = None


def add[E: SQLModel](entity: E, *, instance: str | None = None) -> E:
    """Add: store a new record for an Entity instance and return the created Entity.

    Generated Fields are produced by storage, omitted Fields take their declared
    Default Values, and required and nullability rules are enforced.
    """
    return data.route("add", instance, entity)


def get_by_id[E: SQLModel](
    entity: type[E], id: int, *, instance: str | None = None
) -> E | None:
    """Get by ID: return the record with this ``id``, or ``None`` when none has it."""
    return data.route("get_by_id", instance, entity, id)


def list_[E: SQLModel](
    entity: type[E],
    *,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: str | None = None,
) -> list[E]:
    """List: return the matching records of an Entity class.

    An omitted combination or Order uses the configured default; an omitted limit
    returns every match.
    """
    return data.route(
        "list_",
        instance,
        entity,
        filters=filters,
        combination=combination,
        orders=orders,
        limit=limit,
    )


def update[E: SQLModel](entity: E, *, instance: str | None = None) -> E | None:
    """Update: change the supplied mutable Fields of the record with the Entity's ``id``.

    Returns the updated Entity, or ``None`` when no record has that ``id``.
    """
    return data.route("update", instance, entity)


def delete(entity: type[SQLModel], id: int, *, instance: str | None = None) -> bool:
    """Delete: remove the record with this ``id``; ``True`` when one was removed."""
    return data.route("delete", instance, entity, id)


def enable[E: SQLModel](
    entity: type[E], id: int, *, instance: str | None = None
) -> E | None:
    """Enable: set ``is_active`` to ``True``; ``None`` when no record has this ``id``."""
    return data.route("enable", instance, entity, id)


def disable[E: SQLModel](
    entity: type[E], id: int, *, instance: str | None = None
) -> E | None:
    """Disable: set ``is_active`` to ``False``; ``None`` when no record has this ``id``."""
    return data.route("disable", instance, entity, id)


def count(entity: type[SQLModel], *, instance: str | None = None) -> int:
    """Count: return the number of records, ``0`` when there are none."""
    return data.route("count", instance, entity)


def sum_(entity: type[SQLModel], field: str, *, instance: str | None = None) -> Any:
    """Sum: return the total of a numeric Field, ignoring ``None``; ``0`` when none is usable."""
    return data.route("sum_", instance, entity, field)


def min_(entity: type[SQLModel], field: str, *, instance: str | None = None) -> Any:
    """Min: return the smallest value of a Field, ignoring ``None``; ``None`` when none is usable."""
    return data.route("min_", instance, entity, field)


def max_(entity: type[SQLModel], field: str, *, instance: str | None = None) -> Any:
    """Max: return the largest value of a Field, ignoring ``None``; ``None`` when none is usable."""
    return data.route("max_", instance, entity, field)


def truncate(entity: type[SQLModel], *, instance: str | None = None) -> int:
    """Truncate: remove every record, keep the structure, and return how many were removed."""
    return data.route("truncate", instance, entity)


def execute_command(
    command: str,
    parameters: Mapping[str, Any] | None = None,
    *,
    instance: str | None = None,
) -> CommandResult:
    """Execute Command: run one SQL command and return its Command Result."""
    return data.route("execute_command", instance, command, parameters)
