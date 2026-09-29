"""Storage Action for Database's List Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import DatabaseInstance, Filter, FilterCombination, Order

from logic.core import database as _database


def storage_list(
    entity: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: DatabaseInstance | None = None,
) -> Sequence[Any]:
    """List matching records of an Entity through Database.

    Args:
        entity (Any): Entity class to list.
        filters (Sequence[Filter], optional): Conditions on Entity Fields.
        combination (FilterCombination, optional): How the Filters combine.
        orders (Sequence[Order], optional): Ordering instructions.
        limit (int, optional): Maximum number of records; zero or less means no limit.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (Sequence[Any]): The matching Entity instances.
    """
    return _database.gateway().list(
        entity, filters, combination, orders, limit, instance
    )
