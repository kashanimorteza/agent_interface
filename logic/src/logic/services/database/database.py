"""The Database Service: Database Operations that concern no single Entity."""

from collections.abc import Mapping
from typing import Any

from database.interface import CommandResult, Database

from logic.core.dependency import Dependency
from logic.core.outcome import Outcome


class DatabaseService:
    """Actions that concern the stored data as a whole."""

    def __init__(self, database: Database, dependency: Dependency) -> None:
        """Bind the Service to the Database it reaches and the bounds it works within.

        Args:
            database (Database): Database's published surface.
            dependency (Dependency): Bounded use of the dependency.
        """
        self._database = database
        self._dependency = dependency

    def execute_command(
        self, command: str, parameters: Mapping[str, Any] | None = None
    ) -> Outcome[CommandResult]:
        """Run a command with named bound parameters and return its rows and affected count.

        Args:
            command (str): SQL command using :name parameter markers.
            parameters (Mapping, optional): Value for each named parameter.

        Returns:
            (Outcome): The Command Result, or an invalid failure for a refused command, or an unavailable failure; the command is attempted once because repeating it could change data twice.
        """
        return self._dependency.call(
            lambda: self._database.execute_command(command, parameters)
        )
