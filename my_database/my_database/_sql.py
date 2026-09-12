"""The controlled SQL execution route: a capability-restricted escape hatch
for a data operation the generic Model-driven pipeline cannot express.

Accepts only parameterized values and identifiers already on the internal
allow-list (the tables the Persistence Mapping owns). Rejects any structural
change, privilege change, or migration operation before execution, and
applies the same credential protection to its results as the generic
pipeline.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from my_database._credentials import REDACTED, decrypt_value
from my_database._errors import ControlledSQLRejectedError
from my_database._mapping import MODEL_TO_ORM, credential_fields
from my_database._transactions import transaction

ALLOWED_TABLES: frozenset[str] = frozenset(
    orm_type.__tablename__ for orm_type in MODEL_TO_ORM.values()
)

_REJECTED_KEYWORDS = re.compile(
    r"\b("
    r"CREATE|ALTER|DROP|TRUNCATE|GRANT|REVOKE|ATTACH|DETACH|VACUUM|REINDEX|PRAGMA"
    r")\b",
    re.IGNORECASE,
)

_CREDENTIAL_MODE_BY_TABLE_AND_FIELD: dict[str, dict[str, str]] = {
    orm_type.__tablename__: credential_fields(model_type)
    for model_type, orm_type in MODEL_TO_ORM.items()
}


def _validate(sql: str) -> None:
    if _REJECTED_KEYWORDS.search(sql):
        raise ControlledSQLRejectedError(
            "Controlled SQL rejects structural changes, privilege changes, and migration "
            "operations; use Migration or the generic pipeline instead."
        )
    referenced_identifiers = set(re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", sql))
    # Every allow-listed table actually referenced must be a known table;
    # this does not require every identifier in the statement to be a table
    # name (columns and SQL keywords are also identifiers), only that no
    # FROM/JOIN/INTO/UPDATE target names an unknown table.
    for match in re.finditer(
        r"\b(?:FROM|JOIN|INTO|UPDATE)\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql, re.IGNORECASE
    ):
        table = match.group(1)
        if table not in ALLOWED_TABLES:
            raise ControlledSQLRejectedError(
                f"{table!r} is not an allow-listed table for controlled SQL."
            )
    del referenced_identifiers  # reserved for a future, stricter identifier allow-list


def _protect_row(table: str, row: dict[str, Any]) -> dict[str, Any]:
    modes = _CREDENTIAL_MODE_BY_TABLE_AND_FIELD.get(table, {})
    protected = dict(row)
    for field_name, mode in modes.items():
        if field_name in protected and protected[field_name] is not None:
            protected[field_name] = (
                REDACTED if mode == "hash" else decrypt_value(protected[field_name])
            )
    return protected


def execute_controlled_sql(
    sql: str,
    params: dict[str, Any],
    *,
    table: str,
    instance: str | None = None,
    session: Session | None = None,
) -> Sequence[dict[str, Any]]:
    """Execute one parameterized, allow-listed data operation.

    ``table`` names the single allow-listed table this command targets, used
    to apply the correct credential protection to any returned row.
    """

    _validate(sql)
    if table not in ALLOWED_TABLES:
        raise ControlledSQLRejectedError(f"{table!r} is not an allow-listed table.")

    if session is not None:
        result = session.execute(text(sql), params)
        if result.returns_rows:  # pyright: ignore[reportAttributeAccessIssue]
            return [_protect_row(table, dict(row._mapping)) for row in result]
        return []

    with transaction(instance) as active_session:
        result = active_session.execute(text(sql), params)
        if result.returns_rows:  # pyright: ignore[reportAttributeAccessIssue]
            return [_protect_row(table, dict(row._mapping)) for row in result]
        return []
