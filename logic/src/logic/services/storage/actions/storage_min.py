"""Storage Action for Database's Min Entity Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import Database, DatabaseInstance, Filter, FilterCombination


def storage_min(
    entity: type[Any],
    field: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Return the smallest value of a comparable Field, ignoring nulls; None when nothing matches."""
    return Database().min(entity, field, filters, combination, instance)
