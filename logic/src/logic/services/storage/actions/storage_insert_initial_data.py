"""Storage Action for Database's Insert Initial Data Operation."""

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_insert_initial_data(instance: DatabaseInstance | None = None) -> int:
    """Insert the declared Initial Data through Database.

    Args:
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (int): The number of records inserted.
    """
    return _database.gateway().insert_initial_data(instance)
