"""Tests for Application Outcome and unexpected-failure mapping (task P3-G11-T1)."""

from __future__ import annotations

from backend.config import Settings
from backend.logic.outcomes import ApplicationOutcome
from backend.main import create_app


def test_not_found_outcome_maps_to_404_with_request_id(client, auth_headers) -> None:
    r = client.get("/v1/trading-platform/999999", headers=auth_headers)
    assert r.status_code == 404
    body = r.json()
    assert "request_id" in body
    assert body["request_id"]


def test_validation_failed_outcome_maps_to_422(client, auth_headers) -> None:
    r = client.post("/v1/trading-platform", json={"code": "kraken"}, headers=auth_headers)
    assert r.status_code == 422


def test_unauthenticated_outcome_maps_to_401(client) -> None:
    r = client.get("/v1/trading-platform")
    assert r.status_code == 401


def test_conflict_outcome_maps_to_409(client, auth_headers) -> None:
    client.post("/v1/trading-platform", json={"name": "X", "code": "dup"}, headers=auth_headers)
    r = client.post("/v1/trading-platform", json={"name": "Y", "code": "dup"}, headers=auth_headers)
    # Trading Platform declares no uniqueness in the Target, so this actually succeeds;
    # exercise a Model that does declare uniqueness instead.
    assert r.status_code == 201

    client.post("/v1/action-group", json={"user_id": 1, "name": "Dup"}, headers=auth_headers)
    r2 = client.post("/v1/action-group", json={"user_id": 1, "name": "Dup"}, headers=auth_headers)
    assert r2.status_code == 409
    assert "request_id" in r2.json()


def test_unexpected_failure_produces_safe_generic_response(test_db_config) -> None:
    from fastapi.testclient import TestClient

    fresh_app = create_app(
        Settings(cors_allowed_origins=["https://app.example.test"]), database_config=test_db_config
    )

    @fresh_app.get("/__boom")
    def boom() -> None:
        raise RuntimeError("credential=super-secret should never leak")

    # `raise_server_exceptions=False`: a truly unexpected failure is expected to both
    # produce this safe response to the real caller and still propagate for server-side
    # crash logging (Starlette's ServerErrorMiddleware does both); TestClient's default
    # re-raises it locally for visibility, which this test deliberately disables to
    # observe the response a real caller would receive.
    with TestClient(fresh_app, raise_server_exceptions=False) as client:
        r = client.get("/__boom")
        assert r.status_code == 500
        body = r.json()
        assert body["detail"] == "An unexpected error occurred."
        assert "super-secret" not in r.text
        assert "credential" not in r.text
        assert "request_id" in body


def test_successful_outcome_is_never_reported_as_an_error(client, auth_headers) -> None:
    r = client.post("/v1/trading-platform", json={"name": "OK", "code": "ok"}, headers=auth_headers)
    assert r.status_code == 201
    assert not isinstance(r.json(), ApplicationOutcome)
