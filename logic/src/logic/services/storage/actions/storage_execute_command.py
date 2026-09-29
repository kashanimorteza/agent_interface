"""Storage Action for Database's Execute Command Operation."""

from collections.abc import Mapping
from typing import Any

from database.interface import CommandResult, DatabaseInstance

from logic.core import database as _database


def storage_execute_command(
    command: str,
    parameters: Mapping[str, Any] | None = None,
    instance: DatabaseInstance | None = None,
) -> CommandResult:
    """Execute a SQL command through Database; it is never repeated automatically.

    Args:
        command (str): SQL command to execute.
        parameters (Mapping[str, Any], optional): Named bound parameters.
        instance (DatabaseInstance, optional): Instance to use; Database chooses its default when omitted.

    Returns:
        (CommandResult): Database's Command Result carrying rows and an affected count.
    """
    return _database.gateway().execute_command(command, parameters, instance)
