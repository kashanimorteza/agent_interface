"""Verifies Migration ordering, reversal, integrity, and drift detection."""

from __future__ import annotations

from sqlalchemy import inspect, text

from database.adapter import StorageAdapter
from database.mapping import PERSISTENT_MODELS, table_name
from database.migrations import (
    detect_schema_drift,
    downgrade_to_base,
    upgrade_to_head,
    verify_migration_integrity,
)


def test_upgrade_creates_every_mapped_table(migrated_adapter: StorageAdapter) -> None:
    engine = migrated_adapter.engine_for()
    existing = set(inspect(engine).get_table_names())
    for model_cls in PERSISTENT_MODELS:
        assert table_name(model_cls) in existing


def test_upgrade_leaves_no_structural_drift(migrated_adapter: StorageAdapter) -> None:
    engine = migrated_adapter.engine_for()
    assert detect_schema_drift(engine) == []


def test_downgrade_reverses_every_table(adapter: StorageAdapter) -> None:
    engine = adapter.engine_for()
    upgrade_to_head(engine)
    downgrade_to_base(engine)
    remaining = set(inspect(engine).get_table_names()) - {"alembic_version"}
    assert remaining == set()


def test_recorded_migration_integrity_is_intact() -> None:
    assert verify_migration_integrity() == []


def test_drift_detection_notices_a_missing_table(
    migrated_adapter: StorageAdapter,
) -> None:
    engine = migrated_adapter.engine_for()
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE positions"))
    drift = detect_schema_drift(engine)
    assert any("positions" in entry for entry in drift)
