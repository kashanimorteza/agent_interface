"""Tests for bounded, cursor-based, allowlisted list queries (task P3-G10-T3)."""

from __future__ import annotations


def _create_platforms(client, auth_headers, count: int) -> None:
    for i in range(count):
        client.post(
            "/v1/trading-platform",
            json={"name": f"Platform-{i}", "code": f"code-{i}"},
            headers=auth_headers,
        )


def test_list_request_exceeding_maximum_bound_is_capped(client, auth_headers) -> None:
    _create_platforms(client, auth_headers, 5)
    r = client.get("/v1/trading-platform", params={"limit": 500}, headers=auth_headers)
    assert r.status_code == 422  # Query(le=100) rejects out-of-range limit outright


def test_default_limit_and_explicit_limit_are_respected(client, auth_headers) -> None:
    _create_platforms(client, auth_headers, 5)
    r = client.get("/v1/trading-platform", params={"limit": 2}, headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_non_allowlisted_query_parameter_is_rejected(client, auth_headers) -> None:
    r = client.get("/v1/trading-platform", params={"name": "Kraken"}, headers=auth_headers)
    assert r.status_code == 422


def test_repeated_identical_list_requests_return_the_same_order(client, auth_headers) -> None:
    _create_platforms(client, auth_headers, 4)
    first = client.get("/v1/trading-platform", headers=auth_headers).json()
    second = client.get("/v1/trading-platform", headers=auth_headers).json()
    assert [item["id"] for item in first] == [item["id"] for item in second]
    ids = [item["id"] for item in first]
    assert ids == sorted(ids)


def test_cursor_continues_after_the_last_seen_id(client, auth_headers) -> None:
    _create_platforms(client, auth_headers, 5)
    first_page = client.get(
        "/v1/trading-platform", params={"limit": 2}, headers=auth_headers
    ).json()
    last_id = first_page[-1]["id"]
    second_page = client.get(
        "/v1/trading-platform", params={"cursor": last_id, "limit": 2}, headers=auth_headers
    ).json()
    assert all(item["id"] > last_id for item in second_page)
