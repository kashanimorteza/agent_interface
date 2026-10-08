"""Setup: coordinating the Setup Operations."""

from typing import Any

from . import initial_data, tables
from .data import Selected, select
from .errors import (
    ConnectionFailureError,
    DeclarationMismatchError,
    ExecutionError,
    InvalidInputError,
    SetupError,
)
from .values import SetupResult

_COMMAND_FAILURES = (
    ConnectionFailureError,
    DeclarationMismatchError,
    ExecutionError,
    InvalidInputError,
    SetupError,
)


def _result(
    command: str, selected: Selected, success: bool, affected: int | None, message: str
) -> SetupResult:
    return SetupResult(
        command=command,
        instance=selected.member,
        success=success,
        affected=affected,
        message=f"{command} on the Instance {selected.member.value!r}: {message}",
    )


def _create_tables(selected: Selected) -> SetupResult:
    try:
        created, matching = tables.create(selected)
    except _COMMAND_FAILURES as error:
        return _result("create_tables", selected, False, None, f"failed. {error}")
    return _result(
        "create_tables",
        selected,
        True,
        created + matching,
        f"{created} Tables created, {matching} already matching",
    )


def _insert_initial_data(selected: Selected) -> SetupResult:
    try:
        inserted, skipped = initial_data.insert(selected)
    except _COMMAND_FAILURES as error:
        return _result("insert_initial_data", selected, False, None, f"failed. {error}")
    return _result(
        "insert_initial_data",
        selected,
        True,
        inserted + skipped,
        f"{inserted} records inserted, {skipped} already present",
    )


def create_tables(instance: Any) -> SetupResult:
    """Create the Table of every Entity on the Instance and report a Setup Result."""
    return _create_tables(select(instance))


def insert_initial_data(instance: Any) -> SetupResult:
    """Insert the missing Initial Data on the Instance and report a Setup Result."""
    return _insert_initial_data(select(instance))


def prepare(instance: Any) -> SetupResult:
    """Create the Tables and then insert the Initial Data; stop without inserting when Table creation fails."""
    selected = select(instance)
    created = _create_tables(selected)
    if not created.success:
        return _result("prepare", selected, False, None, f"stopped. {created.message}")
    inserted = _insert_initial_data(selected)
    if not inserted.success:
        return _result("prepare", selected, False, None, f"failed. {inserted.message}")
    return _result(
        "prepare",
        selected,
        True,
        (created.affected or 0) + (inserted.affected or 0),
        f"{created.message}; {inserted.message}",
    )
