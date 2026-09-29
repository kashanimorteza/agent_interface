"""Storage Action forwarding Database's Delete Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_delete(
    entity: Any, record_id: int, instance: DatabaseInstance | None = None
) -> bool:
    """Forward Delete to Database and return its result unchanged."""
    return gateway.database().delete(entity, record_id, instance)
