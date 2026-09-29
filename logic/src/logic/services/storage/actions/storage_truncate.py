"""Storage Action forwarding Database's Truncate Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_truncate(entity: Any, instance: DatabaseInstance | None = None) -> int:
    """Forward Truncate to Database and return its result unchanged."""
    return gateway.database().truncate(entity, instance)
