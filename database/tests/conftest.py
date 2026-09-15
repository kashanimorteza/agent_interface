"""Shared fixtures: a fresh, migrated SQLite Instance for each test that needs one."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

from database.adapter import dispose_all_engines

ROOT = Path(__file__).resolve().parents[1]
DB_FILE = ROOT / "data" / "trading_assistant_general.db"


def alembic_config() -> Config:
    return Config(str(ROOT / "alembic.ini"))


def reset_db_file() -> None:
    dispose_all_engines()
    if DB_FILE.exists():
        DB_FILE.unlink()


@pytest.fixture
def fresh_db() -> Iterator[None]:
    """A freshly migrated, empty Instance. Cleaned up before and after the test."""
    reset_db_file()
    command.upgrade(alembic_config(), "head")
    yield
    reset_db_file()
