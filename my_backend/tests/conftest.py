from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from my_database._base import create_all_tables, get_runtime_config, reset_engine_cache
from my_database._config import sqlite_database_path

import my_backend


@pytest.fixture(autouse=True)
def clean_database():
    reset_engine_cache()
    instance = get_runtime_config().resolve(None)
    db_path = sqlite_database_path(instance)
    if db_path.exists():
        db_path.unlink()
    create_all_tables()
    yield
    reset_engine_cache()


@pytest.fixture
def client():
    app = my_backend.create_app()
    with TestClient(app) as test_client:
        yield test_client
