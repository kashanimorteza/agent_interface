"""Storage Action for Database's Max Entity Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import Database, DatabaseInstance, Filter, FilterCombination


def storage_max(
    entity: type[Any],
    field: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Return the largest value of a comparable Field, ignoring nulls; None when nothing matches."""
    return Database().max(entity, field, filters, combination, instance)
