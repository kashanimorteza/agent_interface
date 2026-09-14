"""Shared pytest fixtures for the Database test suite.

Every test runs against a fresh, isolated SQLite database file so tests never interfere
with each other or with any real data.
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest

from database.db_interface import Database
from database.migrations import upgrade_to_head
from database.runtime_config import EngineProfile, InstanceProfile, RuntimeConfig


@pytest.fixture
def test_config(tmp_path: Path) -> RuntimeConfig:
    """A RuntimeConfig pointed at a throwaway SQLite file unique to this test."""
    unique_name = f"test_{uuid.uuid4().hex[:12]}"
    engine = EngineProfile(key="sqlite", driver="sqlite3", url_scheme="sqlite")
    instance = InstanceProfile(
        key="general",
        name="Test General",
        purpose="Test data.",
        engine="sqlite",
        database=unique_name,
    )
    return RuntimeConfig(
        engines={"sqlite": engine},
        instances={"general": instance},
        default_instance="general",
        data_dir=tmp_path / "data",
    )


def _db_url(config: RuntimeConfig) -> str:
    instance = config.instances[config.default_instance]
    engine = config.engines[instance.engine]
    path = config.storage_path(instance)
    return f"{engine.url_scheme}:///{path}"


@pytest.fixture
def migrated_config(test_config: RuntimeConfig) -> RuntimeConfig:
    """A RuntimeConfig whose Database Instance has had the Migration history applied."""
    upgrade_to_head(db_url=_db_url(test_config))
    return test_config


@pytest.fixture
def db(migrated_config: RuntimeConfig) -> Database:
    return Database(migrated_config, instance=migrated_config.default_instance)
