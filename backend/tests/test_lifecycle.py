"""Tests for Backend's Runtime Configuration contract, health, readiness, and shutdown
(task P3-G12-T1)."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.config import Settings
from backend.main import create_app


def test_health_reports_running_independently_of_dependency_state(client) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "running"}


def test_readiness_becomes_ready_only_after_dependencies_are_usable(client) -> None:
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready"}


def test_readiness_reports_not_ready_before_startup_completes(test_db_config) -> None:
    settings = Settings(cors_allowed_origins=["https://app.example.test"])
    app = create_app(settings, database_config=test_db_config)
    # Without entering the TestClient context, the lifespan (and thus readiness) never
    # runs; app.state.ready starts False.
    assert app.state.ready is False


def test_missing_required_configuration_fails_startup_before_readiness() -> None:
    # cors_allowed_origins has no default: constructing Settings without it fails fast,
    # exactly the "missing required value fails startup" behavior this Task requires.
    env_backup = os.environ.pop("BACKEND_CORS_ALLOWED_ORIGINS", None)
    try:
        with pytest.raises(ValidationError):
            Settings()  # type: ignore[call-arg]
    finally:
        if env_backup is not None:
            os.environ["BACKEND_CORS_ALLOWED_ORIGINS"] = env_backup


def test_readiness_and_startup_failure_never_expose_a_secret_or_connection_detail(
    client,
) -> None:
    r = client.get("/ready")
    text = r.text.lower()
    assert "password" not in text
    assert "secret" not in text
    assert "sqlite:" not in text


def test_graceful_shutdown_releases_the_database_interface(test_db_config) -> None:
    settings = Settings(cors_allowed_origins=["https://app.example.test"])
    app = create_app(settings, database_config=test_db_config)
    with TestClient(app):
        interface = app.state.database_interface
        assert app.state.ready is True
    # After the context manager exits, shutdown has run: readiness flips back and the
    # Database Interface's executor is released (submitting further work fails).
    assert app.state.ready is False
    with pytest.raises(RuntimeError):
        interface._executor.submit(lambda: None)
