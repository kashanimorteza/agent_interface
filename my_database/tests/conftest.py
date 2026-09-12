"""Ensures every test starts from a freshly migrated, empty database."""

from __future__ import annotations

import shutil

import pytest
from alembic import command
from alembic.config import Config

from my_database import _session
from my_database._config import CODE_PATH, DATA_DIR

_ALEMBIC_CONFIG_PATH = CODE_PATH / "alembic.ini"


@pytest.fixture(autouse=True)
def fresh_database() -> None:
    for engine in _session._engines.values():
        engine.dispose()
    _session._engines.clear()
    _session._session_factories.clear()

    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)

    alembic_config = Config(str(_ALEMBIC_CONFIG_PATH))
    command.upgrade(alembic_config, "head")
