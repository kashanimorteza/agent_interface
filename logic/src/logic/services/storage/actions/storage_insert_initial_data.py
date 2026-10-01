"""Storage Action for Database's Insert Initial Data Lifecycle Command."""

from database.interface import Database, DatabaseInstance, LifecycleResult


def storage_insert_initial_data(
    instance: DatabaseInstance | None = None,
) -> LifecycleResult:
    """Insert every missing Initial Data record, skipping identical records and failing on a conflict."""
    return Database().insert_initial_data(instance)
