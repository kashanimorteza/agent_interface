"""Storage Action for Database's Enable Entity Operation."""

from typing import Any

from database.interface import Database, DatabaseInstance


def storage_enable(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Set only is_active to true and return the final Entity, or None when none exists."""
    return Database().enable(entity, id, instance)
