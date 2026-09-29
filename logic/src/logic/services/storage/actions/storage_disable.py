"""Storage Action forwarding Database's Disable Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_disable(
    entity: Any, record_id: int, instance: DatabaseInstance | None = None
) -> Any:
    """Forward Disable to Database and return its result unchanged."""
    return gateway.database().disable(entity, record_id, instance)
