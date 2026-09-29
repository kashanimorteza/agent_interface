"""Storage Action forwarding Database's List Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import DatabaseInstance, Filter, FilterCombination, Order

from logic.services.storage import gateway


def storage_list(
    entity: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: DatabaseInstance | None = None,
) -> Sequence[Any]:
    """Forward List to Database and return its result unchanged."""
    return gateway.database().list(
        entity, filters, combination, orders, limit, instance
    )
