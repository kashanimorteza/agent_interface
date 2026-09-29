"""Storage Action for Database's Truncate Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_truncate(entity: Any, instance: DatabaseInstance | None = None) -> int:
    """Remove every record of an Entity through Database.

    Args:
        entity (Any): Entity class to empty.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (int): The number of deleted records.
    """
    return _database.gateway().truncate(entity, instance)
