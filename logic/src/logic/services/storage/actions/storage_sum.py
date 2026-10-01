"""Storage Action for Database's Sum Entity Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import Database, DatabaseInstance, Filter, FilterCombination


def storage_sum(
    entity: type[Any],
    field: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Return the total of a numeric Field, ignoring nulls; zero when nothing matches."""
    return Database().sum(entity, field, filters, combination, instance)
