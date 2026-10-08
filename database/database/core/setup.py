"""Setup (Core): coordinating the Setup Operations."""

from typing import Any

from database.core import data, initial_data, tables
from database.core.errors import DatabaseError, SetupError
from database.core.values import SetupResult


def create_tables(instance: Any) -> SetupResult:
    return tables.create_tables(instance)


def insert_initial_data(instance: Any) -> SetupResult:
    return initial_data.insert_initial_data(instance)


def prepare(instance: Any) -> SetupResult:
    """Create the Tables, then insert the Initial Data; stop if table creation fails."""
    _, connection, member = data.target(instance)
    try:
        created = tables.create_tables(instance)
    except DatabaseError as error:
        raise SetupError(
            f"prepare stopped: create_tables failed on Instance {connection.instance!r}"
        ) from error
    inserted = initial_data.insert_initial_data(instance)
    return SetupResult(
        command="prepare",
        instance=member,
        success=True,
        affected=(created.affected or 0) + (inserted.affected or 0),
        message=f"{created.message}; {inserted.message}",
    )
