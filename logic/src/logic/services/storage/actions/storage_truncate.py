"""Storage Action for Database's Truncate Entity Operation."""

from typing import Any

from database.interface import Database, DatabaseInstance


def storage_truncate(
    entity: type[Any], instance: DatabaseInstance | None = None
) -> int:
    """Remove every record of the Entity, keep its Table, and return the deleted count."""
    return Database().truncate(entity, instance)
