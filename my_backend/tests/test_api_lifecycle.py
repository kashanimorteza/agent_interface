"""Full CRUD+status lifecycle proven through the external API for two independent entities."""

from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    ("prefix", "payload"),
    [
        ("/trading-platforms", {"name": "MetaTrader 5", "code": "metatrader_5"}),
    ],
)
def test_create_get_list_update_delete_status_round_trip(client, prefix, payload):
    created = client.post(prefix, json=payload)
    assert created.status_code == 201, created.text
    record_id = created.json()["id"]

    fetched = client.get(f"{prefix}/{record_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == record_id

    listed = client.get(prefix)
    assert listed.status_code == 200
    assert any(r["id"] == record_id for r in listed.json())

    updated = client.patch(f"{prefix}/{record_id}", json={"description": "updated"})
    assert updated.status_code == 200
    assert updated.json()["description"] == "updated"
    assert updated.json()["name"] == payload["name"]  # untouched fields preserved

    disabled = client.post(f"{prefix}/{record_id}/status", params={"action": "disable"})
    assert disabled.status_code == 200
    assert disabled.json()["status"] is False

    deleted = client.delete(f"{prefix}/{record_id}")
    assert deleted.status_code == 204
    assert client.get(f"{prefix}/{record_id}").status_code == 404


def test_get_missing_record_returns_404(client):
    resp = client.get("/brokers/999")
    assert resp.status_code == 404


def test_update_missing_record_returns_404(client):
    resp = client.patch("/brokers/999", json={"description": "x"})
    assert resp.status_code == 404


def test_duplicate_unique_field_returns_409(client):
    user_resp = client.post(
        "/users",
        json={"name": "Ada", "username": "ada", "password": "x", "api_key": "y"},
    )
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    first = client.post("/brokers", json={"name": "FxPro", "user_id": user_id})
    assert first.status_code == 201

    second = client.post("/brokers", json={"name": "FxPro", "user_id": user_id})
    assert second.status_code == 409


def test_reference_to_nonexistent_record_returns_409(client):
    resp = client.post("/brokers", json={"name": "Orphan", "user_id": 999})
    assert resp.status_code == 409


def test_partial_update_leaves_omitted_fields_unchanged_and_applies_explicit_null(
    client,
):
    created = client.post(
        "/currencies",
        json={"user_id": 1, "code": "USD", "symbol": "$", "country": "United States"},
    )
    # Currency references user_id=1 which does not exist yet in this test's fresh DB.
    assert created.status_code == 409

    user_resp = client.post(
        "/users",
        json={"name": "Bob", "username": "bob", "password": "x", "api_key": "y"},
    )
    user_id = user_resp.json()["id"]

    created = client.post(
        "/currencies",
        json={
            "user_id": user_id,
            "code": "USD",
            "symbol": "$",
            "country": "United States",
        },
    )
    assert created.status_code == 201
    currency_id = created.json()["id"]

    # Omit "symbol" entirely: unchanged. Explicitly null "country": cleared.
    updated = client.patch(f"/currencies/{currency_id}", json={"country": None})
    assert updated.status_code == 200
    assert updated.json()["symbol"] == "$"
    assert updated.json()["country"] is None


def test_unknown_field_in_create_payload_is_rejected(client):
    resp = client.post(
        "/trading-platforms",
        json={"name": "X", "code": "x", "unexpected": "value"},
    )
    assert resp.status_code == 422
