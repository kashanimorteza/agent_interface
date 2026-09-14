"""Tests for the Storage Adapter Foundation (task P2-G1-T1)."""

from __future__ import annotations

import stat
from pathlib import Path

import pytest

from database.adapter import StorageAdapter
from database.exceptions import ConnectionFailure
from database.runtime_config import EngineProfile, InstanceProfile, RuntimeConfig


def test_foundation_reused_by_more_than_one_mapping_and_the_interface(
    migrated_config: RuntimeConfig,
) -> None:
    import model

    from database.db_interface import Database

    db = Database(migrated_config, instance=migrated_config.default_instance)
    adapter_before = db.adapter
    db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    assert db.adapter is adapter_before  # one Storage Adapter reused, none resolved its own


def test_least_privilege_connection_identity(migrated_config: RuntimeConfig) -> None:
    StorageAdapter(migrated_config, verify_schema=False)
    db_path = migrated_config.storage_path(
        migrated_config.instances[migrated_config.default_instance]
    )
    mode = stat.S_IMODE(db_path.stat().st_mode)
    assert mode == 0o600


def test_connection_failure_produces_signal_with_no_secret_value(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    # A directory where the database file is expected: opening it as a database fails.
    (data_dir / "blocked.db").mkdir()

    engine = EngineProfile(key="sqlite", driver="sqlite3", url_scheme="sqlite")
    instance = InstanceProfile(
        key="general", name="General", purpose="Test.", engine="sqlite", database="blocked"
    )
    config = RuntimeConfig(
        engines={"sqlite": engine},
        instances={"general": instance},
        default_instance="general",
        data_dir=data_dir,
    )

    caplog.set_level("INFO", logger="database.signals")
    with pytest.raises(ConnectionFailure):
        StorageAdapter(config, verify_schema=False)

    assert any("connection_failure" in record.message for record in caplog.records)
    for record in caplog.records:
        assert "secret" not in record.message.lower()
