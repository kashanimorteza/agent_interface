"""Storage Action for Database's Get By Id Entity Operation."""

from typing import Any

from database.interface import Database, DatabaseInstance


def storage_get_by_id(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Return the Entity with the id, or None when none exists."""
    return Database().get_by_id(entity, id, instance)
