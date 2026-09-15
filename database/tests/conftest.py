"""Shared fixtures: an isolated, migrated Storage Adapter and Database Interface per test."""

from __future__ import annotations

import uuid
from collections.abc import Iterator

import pytest
from cryptography.fernet import Fernet

from database.adapter import DEFAULT_DATA_DIR, StorageAdapter
from database.interface import DatabaseInterface
from database.migrations import upgrade_to_head


@pytest.fixture(autouse=True)
def encryption_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "DATABASE_CREDENTIAL_ENCRYPTION_KEY", Fernet.generate_key().decode()
    )


@pytest.fixture
def adapter(tmp_path: object) -> Iterator[StorageAdapter]:
    db_name = f"test_{uuid.uuid4().hex}"
    config_path = tmp_path / "database.yaml"  # type: ignore[attr-defined]
    config_path.write_text(
        "engines:\n"
        '  sqlite:\n    driver: "sqlite"\n'
        "instances:\n"
        "  general:\n"
        '    name: "Test Instance"\n'
        '    purpose: "Isolated test data."\n'
        '    engine: "sqlite"\n'
        f'    database: "{db_name}"\n'
        'default_instance: "general"\n'
    )
    adapter = StorageAdapter(config_path=config_path)
    yield adapter
    db_file = DEFAULT_DATA_DIR / f"{db_name}.db"
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def migrated_adapter(adapter: StorageAdapter) -> StorageAdapter:
    upgrade_to_head(adapter.engine_for())
    return adapter


@pytest.fixture
def db(migrated_adapter: StorageAdapter) -> DatabaseInterface:
    return DatabaseInterface(migrated_adapter)
