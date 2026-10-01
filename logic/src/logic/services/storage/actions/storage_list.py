"""Storage Action for Database's List Entity Operation."""

from collections.abc import Sequence
from typing import Any

from database.interface import (
    Database,
    DatabaseInstance,
    Filter,
    FilterCombination,
    Order,
)


def storage_list(
    entity: type[Any],
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: DatabaseInstance | None = None,
) -> Sequence[Any]:
    """Return the Entities that match, ordered and limited; a zero or negative limit means no limit."""
    return Database().list(entity, filters, combination, orders, limit, instance)
