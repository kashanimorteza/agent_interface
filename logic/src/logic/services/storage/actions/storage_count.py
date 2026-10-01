"""Storage Action for Database's Count Entity Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import Database, DatabaseInstance, Filter, FilterCombination


def storage_count(
    entity: type[Any],
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> int:
    """Return how many Entities match."""
    return Database().count(entity, filters, combination, instance)
