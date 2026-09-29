"""Storage Action for Database's Delete Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_delete(
    entity: Any,
    record_id: int,
    instance: DatabaseInstance | None = None,
) -> bool:
    """Delete a record through Database.

    Args:
        entity (Any): Entity class of the record.
        record_id (int): Id of the record to delete.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (bool): True when a record was deleted and False when no record has that id.
    """
    return _database.gateway().delete(entity, record_id, instance)
