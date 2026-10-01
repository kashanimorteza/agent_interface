"""Storage Action for Database's Create Tables Lifecycle Command."""

from database.interface import Database, DatabaseInstance, LifecycleResult


def storage_create_tables(instance: DatabaseInstance | None = None) -> LifecycleResult:
    """Create every Table from the Model Entities; Database stops on a difference with an existing Table."""
    return Database().create_tables(instance)
