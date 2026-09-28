"""The only public Database layer.

Every Operation names an Entity class or Entity instance directly and accepts an optional Instance.
When the Instance is omitted, Database uses its configured default Instance.
"""

from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from sqlmodel import SQLModel

from database import data
from database.contract import (
    Combination,
    CommandResult,
    Direction,
    Filter,
    Operator,
    Order,
)

__all__ = [
    "Combination",
    "CommandResult",
    "Direction",
    "Filter",
    "Operator",
    "Order",
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


def _submit(
    operation: str, instance: str | None, *arguments: Any, **keywords: Any
) -> Any:
    """Hand a request to Data and return its result."""
    return data.forward(operation, instance, *arguments, **keywords)


def add[T: SQLModel](entity: T, instance: str | None = None) -> T:
    """Add: store a new record.

    Args:
        entity (T): Entity instance for the new record.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (T): The created Entity instance.
    """
    return data.add(entity, instance)


def update[T: SQLModel](entity: T, instance: str | None = None) -> T | None:
    """Update: change the supplied Fields of the record that has the instance's `id`.

    Args:
        entity (T): Entity instance holding the `id` and the changed values.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (T | None): The updated Entity instance, or None when no record has that `id`.
    """
    return data.update(entity, instance)


def delete(
    entity_class: type[SQLModel], record_id: int, instance: str | None = None
) -> bool:
    """Delete: remove one record.

    Args:
        entity_class (type[SQLModel]): Entity class of the record.
        record_id (int): `id` of the record.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (bool): True when a record was removed, False when none has that `id`.
    """
    return data.delete(entity_class, record_id, instance)


def enable[T: SQLModel](
    entity_class: type[T], record_id: int, instance: str | None = None
) -> T | None:
    """Enable: set a record's `is_active` Field to true.

    Args:
        entity_class (type[T]): Entity class of the record.
        record_id (int): `id` of the record.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (T | None): The Entity instance, or None when no record has that `id`.
    """
    return data.enable(entity_class, record_id, instance)


def disable[T: SQLModel](
    entity_class: type[T], record_id: int, instance: str | None = None
) -> T | None:
    """Disable: set a record's `is_active` Field to false.

    Args:
        entity_class (type[T]): Entity class of the record.
        record_id (int): `id` of the record.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (T | None): The Entity instance, or None when no record has that `id`.
    """
    return data.disable(entity_class, record_id, instance)


def truncate(entity_class: type[SQLModel], instance: str | None = None) -> int:
    """Truncate: remove every record of an Entity and keep its Table structure.

    Args:
        entity_class (type[SQLModel]): Entity class to clear.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (int): Number of records removed.
    """
    return data.truncate(entity_class, instance)


def get_by_id[T: SQLModel](
    entity_class: type[T], record_id: int, instance: str | None = None
) -> T | None:
    """Get by ID: return one record.

    Args:
        entity_class (type[T]): Entity class of the record.
        record_id (int): `id` of the record.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (T | None): The Entity instance, or None when no record has that `id`.
    """
    return data.get_by_id(entity_class, record_id, instance)


def list_[T: SQLModel](
    entity_class: type[T],
    *,
    filters: Sequence[Filter] | None = None,
    filter_combination: Combination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: str | None = None,
) -> list[T]:
    """List: return the records of an Entity that satisfy the Filters, ordered and limited as requested.

    Args:
        entity_class (type[T]): Entity class to list.
        filters (Sequence[Filter], optional): Conditions on Entity Fields, each with an Operator enum member and a value.
        filter_combination (Combination, optional): Combination enum member; the configured default when omitted.
        orders (Sequence[Order], optional): Ordering instructions applied in order; the configured default Order when omitted.
        limit (int, optional): Largest number of records to return; every match when omitted.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (list[T]): Matching Entity instances.
    """
    return data.list_(
        entity_class,
        filters=filters,
        filter_combination=filter_combination,
        orders=orders,
        limit=limit,
        instance=instance,
    )


def count(entity_class: type[SQLModel], instance: str | None = None) -> int:
    """Count: return the number of records of an Entity.

    Args:
        entity_class (type[SQLModel]): Entity class to count.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (int): Number of records, 0 when there are none.
    """
    return data.count(entity_class, instance)


def sum_(
    entity_class: type[SQLModel], field: Any, instance: str | None = None
) -> int | float | Decimal:
    """Sum: total a numeric Field, ignoring null values.

    Args:
        entity_class (type[SQLModel]): Entity class to total.
        field (Any): Numeric Field selected from the Entity class.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (int | float | Decimal): The total, or 0 when no usable value exists.
    """
    return data.sum_(entity_class, field, instance)


def min_(entity_class: type[SQLModel], field: Any, instance: str | None = None) -> Any:
    """Min: find the smallest value of a Field, ignoring null values.

    Args:
        entity_class (type[SQLModel]): Entity class to search.
        field (Any): Comparable Field selected from the Entity class.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (Any): The smallest value, or None when no usable value exists.
    """
    return data.min_(entity_class, field, instance)


def max_(entity_class: type[SQLModel], field: Any, instance: str | None = None) -> Any:
    """Max: find the largest value of a Field, ignoring null values.

    Args:
        entity_class (type[SQLModel]): Entity class to search.
        field (Any): Comparable Field selected from the Entity class.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (Any): The largest value, or None when no usable value exists.
    """
    return data.max_(entity_class, field, instance)


def execute_command(
    command: str,
    parameters: Mapping[str, Any] | None = None,
    instance: str | None = None,
) -> CommandResult:
    """Execute Command: run a SQL command through the selected Engine.

    Args:
        command (str): SQL command, with named `:parameter` placeholders.
        parameters (Mapping[str, Any], optional): Values for the placeholders.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (CommandResult): Rows for a command that returns rows, otherwise the affected count.
    """
    return data.execute_command(command, parameters, instance)
