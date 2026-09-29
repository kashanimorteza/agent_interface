"""Storage Action forwarding Database's Add Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_add(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Forward Add to Database and return its result unchanged."""
    return gateway.database().add(entity, instance)
