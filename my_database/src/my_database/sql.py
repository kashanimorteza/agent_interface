"""The controlled, capability-restricted parameterized SQL execution route.

Reserved for data operations the generic pipeline in :mod:`operations` cannot
express. It stays inside the Database boundary: identifiers are checked
against an internal allow-list built from the resolved storage mapping,
values are always bound parameters (never interpolated into the SQL text),
and structural, privilege, and migration commands are rejected before
execution. Results have the same credential redaction as the generic
operations.
"""

from __future__ import annotations

import re

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from . import _session
from ._orm import Base
from .exceptions import ConstraintViolation, UnsupportedOperation
from .transactions import Unit

_ALLOWED_TABLES = frozenset(Base.metadata.tables.keys())
_CREDENTIAL_COLUMNS = frozenset({"password", "api_key"})

_ALLOWED_LEADING_KEYWORDS = ("select", "insert", "update", "delete")
_FORBIDDEN_KEYWORDS = (
    "create",
    "alter",
    "drop",
    "truncate",
    "grant",
    "revoke",
    "attach",
    "detach",
    "pragma",
    "vacuum",
    "reindex",
)

_TABLE_REFERENCE = re.compile(
    r"\b(?:from|into|update|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
    re.IGNORECASE,
)


def _validate_statement(statement: str) -> None:
    stripped = statement.strip().rstrip(";")
    if ";" in stripped:
        raise UnsupportedOperation("controlled SQL accepts exactly one statement")

    leading = stripped.split(None, 1)[0].lower() if stripped else ""
    if leading not in _ALLOWED_LEADING_KEYWORDS:
        raise UnsupportedOperation(
            f"controlled SQL does not support statements starting with {leading!r}"
        )

    lowered = stripped.lower()
    for keyword in _FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lowered):
            raise UnsupportedOperation(f"controlled SQL rejects the {keyword!r} keyword")

    referenced_tables = {match.group(1).lower() for match in _TABLE_REFERENCE.finditer(stripped)}
    unknown = referenced_tables - _ALLOWED_TABLES
    if unknown:
        raise UnsupportedOperation(
            f"controlled SQL references unknown table(s): {', '.join(sorted(unknown))}"
        )


def execute(
    statement: str,
    params: dict | None = None,
    *,
    unit: Unit | None = None,
    instance: str | None = None,
) -> list[dict]:
    """Execute one parameterized, allow-listed, data-only SQL statement.

    ``statement`` uses SQLAlchemy bound-parameter syntax (``:name``); values
    belong in ``params``, never interpolated into ``statement`` itself.
    Returns the fetched rows as protected dictionaries for a ``select``
    statement, or an empty list for a data-changing statement.
    """
    _validate_statement(statement)

    is_select = statement.strip().rstrip(";").split(None, 1)[0].lower() == "select"

    session = unit.session if unit is not None else _session.session_for(instance)
    standalone = unit is None
    try:
        result = session.execute(text(statement), params or {})
        rows: list[dict] = []
        if is_select:
            for row in result.mappings():
                protected = dict(row)
                for column in _CREDENTIAL_COLUMNS:
                    if column in protected and protected[column] is not None:
                        protected[column] = "••••••••"
                rows.append(protected)
        if standalone:
            session.commit()
        return rows
    except IntegrityError as error:
        session.rollback()
        raise ConstraintViolation(str(error)) from error
    except Exception:
        session.rollback()
        raise
    finally:
        if standalone:
            session.close()
