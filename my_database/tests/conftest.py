from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session", autouse=True)
def fresh_migrated_database():
    """Recreate the SQLite data file from a clean state and apply the migration history."""
    data_dir = _PACKAGE_ROOT / "data"
    if data_dir.exists():
        shutil.rmtree(data_dir)

    alembic_cfg = Config(str(_PACKAGE_ROOT / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    yield


@pytest.fixture(scope="session", autouse=True)
def seeded_database(fresh_migrated_database):
    import my_database as db

    counts = db.seed(instance="general")
    yield counts
