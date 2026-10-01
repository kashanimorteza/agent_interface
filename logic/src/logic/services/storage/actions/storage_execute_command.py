"""Storage Action for Database's Execute Command Database-wide Operation."""

from collections.abc import Mapping, Sequence
from typing import Any

from database.interface import CommandResult, Database, DatabaseInstance


def storage_execute_command(
    command: str,
    parameters: Mapping[str, Any] | Sequence[Any] | None = None,
    instance: DatabaseInstance | None = None,
) -> CommandResult:
    """Run a native command in the Instance Engine's query language with bound parameters."""
    return Database().execute_command(command, parameters, instance)
