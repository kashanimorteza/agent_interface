"""Storage Action for Database's Sum Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import DatabaseInstance, Filter, FilterCombination

from logic.core import database as _database


def storage_sum(
    entity: Any,
    field: str,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Total a Field over matching records through Database.

    Args:
        entity (Any): Entity class to aggregate.
        field (str): Name of the Entity Field.
        filters (Sequence[Filter], optional): Conditions on Entity Fields.
        combination (FilterCombination, optional): How the Filters combine.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (Any): That Field's total, or zero when no usable value exists.
    """
    return _database.gateway().sum(entity, field, filters, combination, instance)
