"""Storage Action forwarding Database's Enable Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_enable(
    entity: Any, record_id: int, instance: DatabaseInstance | None = None
) -> Any:
    """Forward Enable to Database and return its result unchanged."""
    return gateway.database().enable(entity, record_id, instance)
