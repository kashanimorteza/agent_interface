"""Tests for the Migration history (task P2-G8-T1)."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect

from database.exceptions import MigrationFailure
from database.mapping import Base
from database.migrations import upgrade_to_head
from database.runtime_config import RuntimeConfig
from database.schema import verify_no_drift


def _db_url(config: RuntimeConfig) -> str:
    instance = config.instances[config.default_instance]
    engine = config.engines[instance.engine]
    return f"{engine.url_scheme}:///{config.storage_path(instance)}"


def test_migration_reproduces_complete_structure_from_empty_database(
    migrated_config: RuntimeConfig,
) -> None:
    engine = create_engine(_db_url(migrated_config))
    inspector = inspect(engine)
    live_tables = set(inspector.get_table_names()) - {"alembic_version"}
    expected_tables = set(Base.metadata.tables)
    assert live_tables == expected_tables

    # Declared constraints reproduced: a representative foreign key and a unique constraint.
    fks = inspector.get_foreign_keys("instances")
    assert any(fk["referred_table"] == "users" for fk in fks)
    uniques = inspector.get_unique_constraints("users")
    assert any("name" in uc["column_names"] for uc in uniques)


def test_drift_detected_before_normal_operations(
    migrated_config: RuntimeConfig, caplog: pytest.LogCaptureFixture
) -> None:
    engine = create_engine(_db_url(migrated_config))
    with engine.begin() as conn:
        conn.exec_driver_sql("ALTER TABLE users ADD COLUMN unexpected_column TEXT")

    caplog.set_level("INFO", logger="database.signals")
    with pytest.raises(MigrationFailure):
        verify_no_drift(engine)
    assert any("migration_failure" in record.message for record in caplog.records)


def test_migration_failure_produces_signal_without_secret_value(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    bogus_url = f"sqlite:///{tmp_path / 'nested' / 'missing' / 'unreachable.db'}"
    caplog.set_level("INFO", logger="database.signals")
    # SQLite auto-creates parent-less files but not missing parent directories, so this
    # deliberately fails: the directory does not exist and is never created for us.
    with pytest.raises(MigrationFailure):
        upgrade_to_head(db_url=bogus_url)
    assert any("migration_failure" in record.message for record in caplog.records)
    for record in caplog.records:
        assert "secret" not in record.message.lower()
