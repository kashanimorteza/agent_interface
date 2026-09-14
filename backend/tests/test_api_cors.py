"""Tests for the CORS allowlist policy (task P3-G10-T4)."""

from __future__ import annotations

from backend.api.cors import cors_middleware_kwargs
from backend.config import Settings
from backend.main import create_app


def test_allowlisted_origin_succeeds(test_db_config) -> None:
    settings = Settings(cors_allowed_origins=["https://app.example.test"])
    app = create_app(settings, database_config=test_db_config)
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        r = client.get(
            "/health",
            headers={"Origin": "https://app.example.test"},
        )
        assert r.headers.get("access-control-allow-origin") == "https://app.example.test"


def test_non_allowlisted_origin_is_rejected(test_db_config) -> None:
    settings = Settings(cors_allowed_origins=["https://app.example.test"])
    app = create_app(settings, database_config=test_db_config)
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        r = client.options(
            "/v1/user",
            headers={
                "Origin": "https://evil.example.test",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert "access-control-allow-origin" not in {k.lower() for k in r.headers}


def test_wildcard_origin_is_never_combined_with_credentialed_access() -> None:
    kwargs = cors_middleware_kwargs(["*"])
    assert kwargs["allow_credentials"] is False

    kwargs = cors_middleware_kwargs(["https://app.example.test"])
    assert kwargs["allow_credentials"] is True
