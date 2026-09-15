"""Schema drift detection.

Maintains one internal (non-public) table holding a deterministic checksum of
the storage structure as reflected directly from the running database,
recorded once when the structure is first established by Migration. Every
later bootstrap call re-reflects the running structure and refuses to
proceed on mismatch, rather than silently repairing drift with an ad-hoc
structural command. Updating the recorded baseline after a deliberate,
recorded Migration is a separate, explicit action (``record_baseline``), so
an unrecorded live change is never mistaken for an authorized one.
"""

from __future__ import annotations

import hashlib

from sqlalchemy import Column, MetaData, String, Table, inspect, select
from sqlalchemy.engine import Engine

from database.exceptions import SchemaDriftError

_INTEGRITY_METADATA = MetaData()

SCHEMA_INTEGRITY_TABLE = Table(
    "_schema_integrity",
    _INTEGRITY_METADATA,
    Column("id", String, primary_key=True),
    Column("checksum", String, nullable=False),
)

_EXCLUDED_TABLES = {"_schema_integrity", "alembic_version"}


def reflect_checksum(engine: Engine, expected_tables: set[str]) -> str:
    """Compute a deterministic checksum of the database's actual live structure."""
    inspector = inspect(engine)
    live_tables = sorted(set(inspector.get_table_names()) & expected_tables)

    parts: list[str] = []
    for table_name in live_tables:
        columns = sorted(inspector.get_columns(table_name), key=lambda c: c["name"])
        col_parts = [
            "|".join(
                [
                    col["name"],
                    str(col["type"]).upper(),
                    str(bool(col.get("nullable", True))),
                ]
            )
            for col in columns
        ]
        uniques = sorted(
            ",".join(sorted(uc["column_names"]))
            for uc in inspector.get_unique_constraints(table_name)
        )
        fks = sorted(
            f"{','.join(fk['constrained_columns'])}->{fk['referred_table']}"
            for fk in inspector.get_foreign_keys(table_name)
        )
        pks = sorted(inspector.get_pk_constraint(table_name).get("constrained_columns") or [])
        parts.append(
            table_name
            + "::"
            + ";".join(col_parts)
            + "::uq="
            + ";".join(uniques)
            + "::fk="
            + ";".join(fks)
            + "::pk="
            + ",".join(pks)
        )
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()


def ensure_integrity_table(engine: Engine) -> None:
    _INTEGRITY_METADATA.create_all(engine, checkfirst=True)


def _stored_checksum(engine: Engine) -> str | None:
    with engine.begin() as conn:
        row = conn.execute(
            select(SCHEMA_INTEGRITY_TABLE.c.checksum).where(
                SCHEMA_INTEGRITY_TABLE.c.id == "current"
            )
        ).first()
    return row[0] if row else None


def record_baseline(engine: Engine, metadata: MetaData) -> None:
    """Record the current live structure as the trusted baseline.

    Called only right after a deliberate, recorded Migration establishes or
    changes the structure — never on an ordinary bootstrap call, so an
    unrecorded live change can never rewrite the trusted baseline.
    """
    ensure_integrity_table(engine)
    expected_tables = set(metadata.tables) - _EXCLUDED_TABLES
    checksum = reflect_checksum(engine, expected_tables)
    with engine.begin() as conn:
        conn.execute(SCHEMA_INTEGRITY_TABLE.delete().where(SCHEMA_INTEGRITY_TABLE.c.id == "current"))
        conn.execute(SCHEMA_INTEGRITY_TABLE.insert().values(id="current", checksum=checksum))


def verify(engine: Engine, metadata: MetaData) -> None:
    """Verify the running structure still matches the recorded baseline."""
    ensure_integrity_table(engine)
    expected_tables = set(metadata.tables) - _EXCLUDED_TABLES
    stored = _stored_checksum(engine)
    if stored is None:
        record_baseline(engine, metadata)
        return
    current = reflect_checksum(engine, expected_tables)
    if stored != current:
        raise SchemaDriftError(
            "The running storage structure does not match the recorded Migration "
            "history's baseline checksum. Reconcile through a recorded Migration; "
            "the running structure was not repaired automatically."
        )
