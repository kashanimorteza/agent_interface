"""Storage Action for Database's Prepare Lifecycle Command."""

from database.interface import Database, DatabaseInstance, LifecycleResult


def storage_prepare(instance: DatabaseInstance | None = None) -> LifecycleResult:
    """Run Create Tables and then Insert Initial Data, stopping when Create Tables fails."""
    return Database().prepare(instance)
