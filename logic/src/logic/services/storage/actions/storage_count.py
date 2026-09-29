"""Storage Action forwarding Database's Count Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import DatabaseInstance, Filter, FilterCombination

from logic.services.storage import gateway


def storage_count(
    entity: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> int:
    """Forward Count to Database and return its result unchanged."""
    return gateway.database().count(entity, filters, combination, instance)
