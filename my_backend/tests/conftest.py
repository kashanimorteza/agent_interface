"""Ensures every test starts from a freshly migrated, empty database and a
fresh FastAPI TestClient.
"""

from __future__ import annotations

import shutil

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from my_database import _session
from my_database._config import CODE_PATH as DATABASE_CODE_PATH
from my_database._config import DATA_DIR

from my_backend.app import create_app

_ALEMBIC_CONFIG_PATH = DATABASE_CODE_PATH / "alembic.ini"


@pytest.fixture(autouse=True)
def fresh_database() -> None:
    for engine in _session._engines.values():
        engine.dispose()
    _session._engines.clear()
    _session._session_factories.clear()

    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)

    alembic_config = Config(str(_ALEMBIC_CONFIG_PATH))
    # The ini's script_location is relative to my_database/'s own working
    # directory; make it absolute so it resolves correctly when tests run
    # from my_backend/'s working directory instead.
    alembic_config.set_main_option(
        "script_location", str(DATABASE_CODE_PATH / "my_database" / "alembic")
    )
    command.upgrade(alembic_config, "head")


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())
