"""Storage Action for Database's Disable Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_disable(
    entity: Any,
    record_id: int,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Mark a record inactive through Database.

    Args:
        entity (Any): Entity class of the record.
        record_id (int): Id of the record to disable.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (Any): The Entity instance, or None when no record has that id.
    """
    return _database.gateway().disable(entity, record_id, instance)
