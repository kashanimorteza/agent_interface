"""Tables (Core): the create-tables Setup Operation."""

from typing import Any

from model import entities

from database.core import data
from database.core.values import SetupResult


def create_tables(instance: Any) -> SetupResult:
    """Create every Table of the Model Entity Collection on the Instance."""
    engine, connection, member = data.target(instance)
    created = engine.create_tables(connection, entities)
    return SetupResult(
        command="create_tables",
        instance=member,
        success=True,
        affected=created,
        message=f"{created} Tables created, {len(entities) - created} already present",
    )
