"""Storage Action for Database's Delete Entity Operation."""

from typing import Any

from database.interface import Database, DatabaseInstance


def storage_delete(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Delete the record with the id and return it as it was, or None when none exists."""
    return Database().delete(entity, id, instance)
