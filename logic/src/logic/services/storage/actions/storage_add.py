"""Storage Action for Database's Add Entity Operation."""

from typing import Any

from database.interface import Database, DatabaseInstance


def storage_add(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Store one complete new Entity instance and return the stored Entity."""
    return Database().add(entity, instance)
