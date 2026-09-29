"""Storage Action for Database's Count Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import DatabaseInstance, Filter, FilterCombination

from logic.core import database as _database


def storage_count(
    entity: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> int:
    """Count matching records through Database.

    Args:
        entity (Any): Entity class to count.
        filters (Sequence[Filter], optional): Conditions on Entity Fields.
        combination (FilterCombination, optional): How the Filters combine.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (int): The number of matching records.
    """
    return _database.gateway().count(entity, filters, combination, instance)
