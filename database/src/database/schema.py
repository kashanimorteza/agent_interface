"""Schema integrity: a checksum of the mapped structure and drift detection against the
running Database, performed before normal data operations (Database Principle 15)."""

from __future__ import annotations

import hashlib

from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from . import observability
from .exceptions import MigrationFailure
from .mapping import Base

_Signature = tuple[tuple[str, str, str, bool], ...]


def _expected_signature() -> _Signature:
    rows = []
    for table in sorted(Base.metadata.tables.values(), key=lambda t: t.name):
        for column in sorted(table.columns, key=lambda c: c.name):
            rows.append((table.name, column.name, str(column.type), bool(column.nullable)))
    return tuple(rows)


def _live_signature(engine: Engine) -> _Signature:
    inspector = inspect(engine)
    rows = []
    for table_name in sorted(inspector.get_table_names()):
        if table_name in ("alembic_version",):
            continue
        for column in sorted(inspector.get_columns(table_name), key=lambda c: c["name"]):
            rows.append((table_name, column["name"], str(column["type"]), bool(column["nullable"])))
    return tuple(rows)


def checksum(signature: _Signature) -> str:
    return hashlib.sha256(repr(signature).encode("utf-8")).hexdigest()


def expected_checksum() -> str:
    return checksum(_expected_signature())


def live_checksum(engine: Engine) -> str:
    return checksum(_live_signature(engine))


def verify_no_drift(engine: Engine) -> None:
    """Raise MigrationFailure and record a signal if the running structure has drifted
    from the structure the recorded Migration history establishes."""
    expected = expected_checksum()
    live = live_checksum(engine)
    if expected != live:
        observability.migration_failure(
            f"schema drift detected: expected={expected[:12]} live={live[:12]}"
        )
        raise MigrationFailure(
            "The running Database structure has drifted from the recorded Migration history"
        )
