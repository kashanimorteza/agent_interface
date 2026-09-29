"""Storage Action forwarding Database's Insert Initial Data Operation."""

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_insert_initial_data(instance: DatabaseInstance | None = None) -> int:
    """Forward Insert Initial Data to Database and return its result unchanged."""
    return gateway.database().insert_initial_data(instance)
