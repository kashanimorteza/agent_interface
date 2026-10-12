"""create_tables: the Tables of the Model Entity Collection."""

from typing import Any

from model.interface import entities
from sqlalchemy import Table

from database.core.data import resolve
from database.core.errors import DatabaseError
from database.core.values import SetupResult

COMMAND = "create_tables"


def _table(entity: Any) -> Table:
    return entity.__table__


def create_tables(instance: Any = None) -> SetupResult:
    """Create every Table from the Entities and their Declarations, using nothing else."""
    member, resolved, unit = resolve(instance)
    tables = tuple(_table(entity) for entity in entities)
    try:
        created = unit.create_tables(resolved, tables)
    except DatabaseError as error:
        return SetupResult(
            command=COMMAND,
            instance=member,
            success=False,
            affected=None,
            message=str(error),
        )
    return SetupResult(
        command=COMMAND,
        instance=member,
        success=True,
        affected=len(tables),
        message=f"{created} Tables created, {len(tables) - created} already matched",
    )
