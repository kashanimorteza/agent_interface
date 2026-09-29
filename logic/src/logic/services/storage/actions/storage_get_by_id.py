"""Storage Action forwarding Database's Get by ID Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_get_by_id(
    entity: Any, record_id: int, instance: DatabaseInstance | None = None
) -> Any:
    """Forward Get by ID to Database and return its result unchanged."""
    return gateway.database().get_by_id(entity, record_id, instance)
