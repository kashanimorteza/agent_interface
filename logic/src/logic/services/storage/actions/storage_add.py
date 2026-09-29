"""Storage Action for Database's Add Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_add(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Persist a complete Entity instance through Database.

    Args:
        entity (Any): Complete Entity instance for the new record.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (Any): The created Entity instance, including Database-generated values.
    """
    return _database.gateway().add(entity, instance)
