"""Storage Action forwarding Database's Execute Command Operation."""

from collections.abc import Mapping
from typing import Any

from database.interface import CommandResult, DatabaseInstance

from logic.services.storage import gateway


def storage_execute_command(
    command: str,
    parameters: Mapping[str, Any] | None = None,
    instance: DatabaseInstance | None = None,
) -> CommandResult:
    """Forward Execute Command to Database and return its result unchanged."""
    return gateway.database().execute_command(command, parameters, instance)
