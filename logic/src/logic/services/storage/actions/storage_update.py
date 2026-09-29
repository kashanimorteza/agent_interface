"""Storage Action forwarding Database's Update Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_update(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Forward Update to Database and return its result unchanged."""
    return gateway.database().update(entity, instance)
