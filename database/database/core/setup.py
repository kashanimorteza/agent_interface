"""The coordination of the Setup Operations, including Prepare."""

from typing import Any

from database.core import initial_data, tables
from database.core.configuration import database_instance, resolve_instance
from database.core.errors import DatabaseError
from database.core.values import SetupResult


class Setup:
    """Runs every Setup Operation on the selected Instance."""

    def create_tables(self, instance: Any = None) -> SetupResult:
        return tables.create_tables(instance)

    def insert_initial_data(self, instance: Any = None) -> SetupResult:
        return initial_data.insert_initial_data(instance)

    def prepare(self, instance: Any = None) -> SetupResult:
        """Create the Tables and then insert the Initial Data; stop without inserting when creation fails."""
        member = database_instance(resolve_instance(instance).key)
        try:
            created = tables.create_tables(instance)
        except DatabaseError as error:
            return SetupResult(
                "prepare",
                member,
                False,
                None,
                f"create_tables did not complete: {error}",
            )
        try:
            inserted = initial_data.insert_initial_data(instance)
        except DatabaseError as error:
            return SetupResult(
                "prepare",
                member,
                False,
                created.affected,
                f"insert_initial_data did not complete: {error}",
            )
        return SetupResult(
            "prepare",
            member,
            True,
            (created.affected or 0) + (inserted.affected or 0),
            f"{created.message} {inserted.message}",
        )
