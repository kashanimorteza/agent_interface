"""Storage Action for Database's Update Entity Operation."""

from typing import Any

from database.interface import Database, DatabaseInstance


def storage_update(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Replace the mutable Fields of the stored record the Entity's id locates; return the stored Entity or None."""
    return Database().update(entity, instance)
