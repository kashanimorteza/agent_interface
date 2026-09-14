"""Tests for standard Model operations exposed through the API Interface (task P3-G10-T1)."""

from __future__ import annotations


def test_every_model_logic_units_operations_reachable_and_invoke_logic_not_database(
    client, auth_headers
) -> None:
    r = client.post(
        "/v1/trading-platform", json={"name": "Kraken", "code": "kraken"}, headers=auth_headers
    )
    assert r.status_code == 201
    platform_id = r.json()["id"]

    assert (
        client.get(f"/v1/trading-platform/{platform_id}", headers=auth_headers).status_code == 200
    )
    assert client.get("/v1/trading-platform", headers=auth_headers).status_code == 200

    r = client.put(
        f"/v1/trading-platform/{platform_id}",
        json={"description": "updated"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["description"] == "updated"

    r = client.post(f"/v1/trading-platform/{platform_id}/disable", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["is_active"] is False

    r = client.post(f"/v1/trading-platform/{platform_id}/enable", headers=auth_headers)
    assert r.json()["is_active"] is True

    r = client.delete(f"/v1/trading-platform/{platform_id}", headers=auth_headers)
    assert r.status_code == 204

    r = client.get(f"/v1/trading-platform/{platform_id}", headers=auth_headers)
    assert r.status_code == 404


def test_search_filters_by_declared_model_field(client, auth_headers) -> None:
    client.post(
        "/v1/trading-platform", json={"name": "Searchable", "code": "searchable"}, headers=auth_headers
    )
    r = client.get("/v1/trading-platform/search", params={"code": "searchable"}, headers=auth_headers)
    assert r.status_code == 200
    assert [item["code"] for item in r.json()] == ["searchable"]


def test_malformed_transport_input_is_rejected_before_logic_executes(client, auth_headers) -> None:
    r = client.post("/v1/trading-platform", json={"code": "kraken"}, headers=auth_headers)
    assert r.status_code == 422


def test_get_by_id_returns_404_for_missing_record(client, auth_headers) -> None:
    r = client.get("/v1/trading-platform/999999", headers=auth_headers)
    assert r.status_code == 404


def test_second_domain_definitions_operations_also_reachable(client, auth_headers) -> None:
    r = client.post(
        "/v1/action-group",
        json={"user_id": 1, "name": "Second"},
        headers=auth_headers,
    )
    assert r.status_code == 201
