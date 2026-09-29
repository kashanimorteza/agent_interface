"""Storage Action forwarding Database's Create Tables Operation."""

from database.interface import DatabaseInstance

from logic.services.storage import gateway


def storage_create_tables(instance: DatabaseInstance | None = None) -> None:
    """Forward Create Tables to Database and return its result unchanged."""
    return gateway.database().create_tables(instance)
