"""The controlled route for work the generic operations cannot express.

This is the one exception to definition-driven access, and it is narrow on
purpose. Before a command runs, this establishes what it can reach and whether
the protections that hold for every other operation can hold for it too. If they
cannot, the command is refused rather than run carefully.

Structural change never comes through here: how the structure came to be is the
recorded history's business alone.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

from sqlalchemy import Connection, text

from ..contract import CommandRefused, CommandResult
from . import credentials, mapping
from .operations import validate_stored


_STRUCTURAL = (
    "create", "alter", "drop", "truncate", "rename", "attach", "detach",
    "vacuum", "reindex", "pragma", "grant", "revoke",
)
_READING = ("select", "with")
_WRITING = ("insert", "update", "delete", "replace")

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_COMMENT = re.compile(r"--[^\n]*|/\*.*?\*/", re.S)
_STRING = re.compile(r"'(?:[^']|'')*'")
# A star standing for "every column", as opposed to one inside a count or a
# multiplication: those name no column and expose nothing.
_COUNTING = re.compile(r"\(\s*\*\s*\)")
_EVERY_COLUMN = re.compile(r"(?:\bselect\b|,)\s*(?:[A-Za-z_][A-Za-z0-9_]*\s*\.\s*)?\*", re.I)


def _bare(statement: str) -> str:
    """The statement with its comments and quoted text removed."""

    return _STRING.sub(" ", _COMMENT.sub(" ", statement))


def _verb(statement: str) -> str:
    stripped = _bare(statement).strip().lower()
    return stripped.split()[0] if stripped.split() else ""


def _tables_named(statement: str) -> tuple[set[str], set[str]]:
    """The known and unknown table names a statement mentions."""

    known = {table.name: table for table in mapping.TABLES.values()}
    words = {word.lower() for word in _IDENTIFIER.findall(_bare(statement))}
    named = {name for name in words if name in known}

    # A word in the position of a table that names no table we hold.
    positions = re.findall(
        r"\b(?:from|join|into|update|table)\s+([A-Za-z_][A-Za-z0-9_]*)",
        _bare(statement),
        re.I,
    )
    unknown = {name.lower() for name in positions if name.lower() not in known}
    return named, unknown


def _credential_columns(table_names: set[str]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for entity_name, table in mapping.TABLES.items():
        if table.name not in table_names:
            continue
        entity = mapping.entity_named(entity_name)
        fields = set(credentials.treatments(entity))
        if fields:
            found[table.name] = fields
    return found


def inspect(statement: str, *, engine_specific: str | None, engine: str) -> tuple[str, set[str]]:
    """Establish what a command may do, or refuse it before it runs."""

    if engine_specific is not None and engine_specific != engine:
        raise CommandRefused(
            f"this command is written for the {engine_specific!r} engine, and the selected "
            f"Instance is reached through {engine!r}"
        )

    bare = _bare(statement).strip().rstrip(";")
    if ";" in bare:
        raise CommandRefused("a command carries one statement, not several")

    verb = _verb(statement)
    if verb in _STRUCTURAL:
        raise CommandRefused(
            f"{verb!r} changes the structure, which only the recorded history may do"
        )
    if verb not in (*_READING, *_WRITING):
        raise CommandRefused(f"{verb or 'an empty command'!r} is not a data operation")

    named, unknown = _tables_named(statement)
    if unknown:
        raise CommandRefused(
            f"this command names {sorted(unknown)}, which this layer holds nothing for"
        )
    if not named:
        raise CommandRefused("this command names nothing this layer holds")

    protected = _credential_columns(named)
    words = {word.lower() for word in _IDENTIFIER.findall(_bare(statement))}
    for table_name, fields in protected.items():
        touched = fields & words
        if touched:
            raise CommandRefused(
                f"this command names {sorted(touched)} of {table_name}, which is held under a "
                f"credential treatment this route cannot preserve"
            )
        if verb in _READING and _EVERY_COLUMN.search(_COUNTING.sub("()", _bare(statement))):
            raise CommandRefused(
                f"this command would return every column of {table_name}, including a "
                f"credential's stored form; name the columns it needs instead"
            )

    return verb, named


def run(
    connection: Connection,
    statement: str,
    parameters: Mapping[str, Any] | None = None,
    *,
    engine: str,
    engine_specific: str | None = None,
) -> CommandResult:
    """Run a command under the protections every other operation holds.

    Values arrive as parameters and stay values. A command that changes data is
    judged by the definitions it touched before its changes are allowed to
    stand, in the same unit of work, so a failure leaves nothing behind.
    """

    verb, named = inspect(statement, engine_specific=engine_specific, engine=engine)
    result = connection.execute(text(statement), dict(parameters or {}))

    rows: tuple[Mapping[str, Any], ...] = ()
    changed = 0
    if result.returns_rows:
        rows = tuple(dict(row) for row in result.mappings().all())
        for row in rows:
            for value in row.values():
                if credentials.is_stored_form(value):
                    raise CommandRefused(
                        "this command returned the stored form of a credential"
                    )
    else:
        changed = result.rowcount

    if verb in _WRITING:
        for entity_name, table in mapping.TABLES.items():
            if table.name not in named:
                continue
            entity = mapping.entity_named(entity_name)
            for row in connection.execute(table.select()).mappings():
                validate_stored(entity, row)

    return CommandResult(rows=rows, changed=changed)


__all__ = ["CommandRefused", "CommandResult", "run"]
