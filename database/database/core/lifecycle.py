"""Core Lifecycle: the Prepare command, which runs CreateTables and then InsertInitialData."""

from database.core.data import Data
from database.core.initial_data import insert_initial_data
from database.core.tables import create_tables
from database.core.values import DatabaseInstance, LifecycleResult

COMMAND = "prepare"


def prepare(data: Data, instance: DatabaseInstance | None) -> LifecycleResult:
    """Create the Tables, then insert the Initial Data; stop if the Tables cannot be created."""
    tables = create_tables(data, instance)
    if not tables.success:
        message = f"Stopped, create_tables failed: {tables.message}"
        return LifecycleResult(COMMAND, tables.instance, False, tables.affected, message)
    records = insert_initial_data(data, instance)
    processed = (tables.affected or 0) + (records.affected or 0)
    message = f"{tables.message}; {records.message}"
    return LifecycleResult(COMMAND, records.instance, records.success, processed, message)
