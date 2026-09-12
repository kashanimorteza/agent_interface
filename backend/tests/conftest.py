from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

_MY_DATABASE_ROOT = Path(__file__).resolve().parent.parent.parent / "my_database"


@pytest.fixture(scope="session", autouse=True)
def fresh_migrated_seeded_database():
    """Recreate my_database's SQLite file from a clean state, migrate, and seed it."""
    data_dir = _MY_DATABASE_ROOT / "data"
    if data_dir.exists():
        shutil.rmtree(data_dir)

    alembic_cfg = Config(str(_MY_DATABASE_ROOT / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(_MY_DATABASE_ROOT / "migrations"))
    command.upgrade(alembic_cfg, "head")

    import my_database as db

    counts = db.seed(instance="general")
    yield counts


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    from backend import app

    return TestClient(app)
