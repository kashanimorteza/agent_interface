"""Storage Action for Database's Create Tables Operation."""

from database.interface import DatabaseInstance

from logic.core import database as _database


def storage_create_tables(instance: DatabaseInstance | None = None) -> None:
    """Create or migrate the Tables the Model Entities require through Database.

    Args:
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (None): Nothing.
    """
    return _database.gateway().create_tables(instance)
