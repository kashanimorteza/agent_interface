"""Storage Action forwarding Database's Sum Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import DatabaseInstance, Filter, FilterCombination

from logic.services.storage import gateway


def storage_sum(
    entity: Any,
    field: str,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Forward Sum to Database and return its result unchanged."""
    return gateway.database().sum(entity, field, filters, combination, instance)
