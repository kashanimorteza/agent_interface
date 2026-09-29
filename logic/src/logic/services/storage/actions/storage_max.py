"""Storage Action for Database's Max Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import DatabaseInstance, Filter, FilterCombination

from logic.core import database as _database


def storage_max(
    entity: Any,
    field: str,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Find the largest value of a Field over matching records through Database.

    Args:
        entity (Any): Entity class to aggregate.
        field (str): Name of the Entity Field.
        filters (Sequence[Filter], optional): Conditions on Entity Fields.
        combination (FilterCombination, optional): How the Filters combine.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (Any): The largest usable value, or None when none exists.
    """
    return _database.gateway().max(entity, field, filters, combination, instance)
