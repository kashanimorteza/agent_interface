"""Schema-drift detection: compares the live database against the resolved ORM mapping.

Internal Development/operational tooling, run before normal operation per
Database Preferences ``implementation.migrations.drift_detection``.
"""

from __future__ import annotations

from sqlalchemy import Engine, inspect

from ._orm import Base


def detect_drift(engine: Engine) -> list[str]:
    """Return human-readable schema differences between the live database and the
    current ORM mapping. An empty list means the live schema matches exactly.
    """
    inspector = inspect(engine)
    live_tables = set(inspector.get_table_names())
    expected_tables = set(Base.metadata.tables.keys())

    differences: list[str] = []
    missing = expected_tables - live_tables
    extra = live_tables - expected_tables - {"alembic_version"}
    if missing:
        differences.append(f"missing tables: {sorted(missing)}")
    if extra:
        differences.append(f"unexpected tables: {sorted(extra)}")

    for table_name in sorted(expected_tables & live_tables):
        expected_cols = {c.name for c in Base.metadata.tables[table_name].columns}
        live_cols = {c["name"] for c in inspector.get_columns(table_name)}
        if expected_cols != live_cols:
            expected_sorted = sorted(expected_cols)
            live_sorted = sorted(live_cols)
            differences.append(
                f"{table_name}: column mismatch expected={expected_sorted} live={live_sorted}"
            )

    return differences
