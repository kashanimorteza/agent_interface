"""Shared pytest fixtures for the Backend test suite.

Sets DATABASE_COMPONENT_ROOT before any import of `backend` or `database` so Database
resolves its runtime configuration against the real sibling `database/` component root
rather than this package's own installed (non-editable) location.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator
from pathlib import Path

_DATABASE_ROOT = (Path(__file__).resolve().parents[2] / "database").resolve()
os.environ.setdefault("DATABASE_COMPONENT_ROOT", str(_DATABASE_ROOT))
# `backend.main` builds a module-level `app` via `create_app()` at import time (the
# official executable entry point), which validates Settings immediately. Tests never
# use that module-level app (each builds its own via the `app` fixture below with an
# isolated database_config), but importing the module still requires valid settings.
os.environ.setdefault("BACKEND_CORS_ALLOWED_ORIGINS", '["https://app.example.test"]')

import pytest  # noqa: E402
from database.db_interface import Database  # noqa: E402
from database.migrations import upgrade_to_head  # noqa: E402
from database.runtime_config import EngineProfile, InstanceProfile, RuntimeConfig  # noqa: E402
from database.seed import seed_initial_data  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from backend.config import Settings  # noqa: E402
from backend.main import create_app  # noqa: E402


def _db_url(config: RuntimeConfig) -> str:
    instance = config.instances[config.default_instance]
    engine = config.engines[instance.engine]
    return f"{engine.url_scheme}:///{config.storage_path(instance)}"


@pytest.fixture
def test_db_config(tmp_path: Path) -> RuntimeConfig:
    """A fresh, isolated, migrated RuntimeConfig unique to this test."""
    unique_name = f"test_{uuid.uuid4().hex[:12]}"
    engine = EngineProfile(key="sqlite", driver="sqlite3", url_scheme="sqlite")
    instance = InstanceProfile(
        key="general",
        name="Test General",
        purpose="Test data.",
        engine="sqlite",
        database=unique_name,
    )
    config = RuntimeConfig(
        engines={"sqlite": engine},
        instances={"general": instance},
        default_instance="general",
        data_dir=tmp_path / "data",
    )
    upgrade_to_head(db_url=_db_url(config))
    return config


@pytest.fixture
def db(test_db_config: RuntimeConfig) -> Database:
    return Database(test_db_config, instance=test_db_config.default_instance)


@pytest.fixture
def seeded_credentials(db: Database) -> dict[str, str]:
    return seed_initial_data(db)


@pytest.fixture
def settings() -> Settings:
    return Settings(cors_allowed_origins=["https://app.example.test"])


@pytest.fixture
def app(test_db_config: RuntimeConfig, settings: Settings) -> Iterator[FastAPI]:
    application = create_app(settings, database_config=test_db_config)
    with TestClient(application):
        yield application


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def admin_api_key(db: Database, seeded_credentials: dict[str, str]) -> str:
    return seeded_credentials["admin_api_key"]


@pytest.fixture
def auth_headers(admin_api_key: str) -> dict[str, str]:
    return {"X-API-Key": admin_api_key}
