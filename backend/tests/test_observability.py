"""Tests for request correlation and safe operational logging (task P3-G12-T2)."""

from __future__ import annotations

import pytest


def test_generated_request_id_appears_in_the_response_header(client, auth_headers) -> None:
    r = client.get("/v1/user", headers=auth_headers)
    assert "X-Request-ID" in r.headers
    assert r.headers["X-Request-ID"]


def test_incoming_request_id_is_honored(client, auth_headers) -> None:
    headers = {**auth_headers, "X-Request-ID": "my-custom-id"}
    r = client.get("/v1/user", headers=headers)
    assert r.headers["X-Request-ID"] == "my-custom-id"


def test_logs_are_correlated_by_the_request_id(
    client, auth_headers, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("INFO", logger="backend.requests")
    headers = {**auth_headers, "X-Request-ID": "correlate-me"}
    r = client.get("/v1/user", headers=headers)
    assert r.status_code == 200
    request_ids = [getattr(record, "request_id", None) for record in caplog.records]
    assert "correlate-me" in request_ids


def test_error_response_carries_the_request_id(client) -> None:
    r = client.get("/v1/user")  # unauthenticated -> 401
    assert r.status_code == 401
    body = r.json()
    assert body["request_id"] == r.headers["X-Request-ID"]


def test_no_credential_or_secret_value_present_in_logs(
    client, auth_headers, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("INFO")
    client.post(
        "/v1/instance",
        json={
            "user_id": 1,
            "name": "MyInstance",
            "trading_platform_id": 1,
            "password": "top-secret-password",
            "api_key": "top-secret-key",
        },
        headers=auth_headers,
    )
    for record in caplog.records:
        assert "top-secret-password" not in record.getMessage()
        assert "top-secret-key" not in record.getMessage()
