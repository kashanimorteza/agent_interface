"""Coordinating the Setup Operations, including prepare."""

from typing import Any

from database.core.data import resolve
from database.core.initial_data import insert_initial_data
from database.core.tables import create_tables
from database.core.values import SetupResult

COMMAND = "prepare"


def prepare(instance: Any = None) -> SetupResult:
    """Run create_tables and then insert_initial_data; stop when create_tables fails."""
    member, _, _ = resolve(instance)
    tables = create_tables(member)
    if not tables.success:
        return SetupResult(
            command=COMMAND,
            instance=member,
            success=False,
            affected=None,
            message=f"create_tables failed; insert_initial_data not run: {tables.message}",
        )
    records = insert_initial_data(member)
    return SetupResult(
        command=COMMAND,
        instance=member,
        success=records.success,
        affected=records.affected,
        message=f"{tables.message}; {records.message}",
    )
