"""Storage Action for Database's Update Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_update(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Replace the mutable Fields of an existing record through Database.

    Args:
        entity (Any): Complete Entity instance for the existing record.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (Any): The updated Entity instance, or None when no record has that id.
    """
    return _database.gateway().update(entity, instance)
