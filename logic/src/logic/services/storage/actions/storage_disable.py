"""Storage Action for Database's Disable Entity Operation."""

from typing import Any

from database.interface import Database, DatabaseInstance


def storage_disable(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Set only is_active to false and return the final Entity, or None when none exists."""
    return Database().disable(entity, id, instance)
