"""Storage Action for Database's Get by ID Operation."""

from typing import Any

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_get_by_id(
    entity: Any,
    record_id: int,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Retrieve one record by its id through Database.

    Args:
        entity (Any): Entity class of the record.
        record_id (int): Id of the record to retrieve.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (Any): The matching Entity instance, or None when no record has that id.
    """
    return _database.gateway().get_by_id(entity, record_id, instance)
