"""End-to-end API checks: standard operations, Credential protection, and
error mapping across multiple distinct Models (Task P3-T4, P3-T6).
"""

from __future__ import annotations


def test_create_read_update_delete_cycle_for_broker(client):
    created = client.post("/brokers", json={"name": "Cycle Broker", "user_id": 1})
    assert created.status_code == 201
    broker_id = created.json()["id"]

    fetched = client.get(f"/brokers/{broker_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Cycle Broker"

    updated = client.patch(f"/brokers/{broker_id}", json={"description": "updated"})
    assert updated.status_code == 200
    assert updated.json()["description"] == "updated"
    assert updated.json()["name"] == "Cycle Broker"  # omitted field unchanged

    deleted = client.delete(f"/brokers/{broker_id}")
    assert deleted.status_code == 204

    gone = client.get(f"/brokers/{broker_id}")
    assert gone.status_code == 404


def test_create_read_update_delete_cycle_for_currency(client):
    created = client.post("/currencies", json={"user_id": 1, "code": "XTS"})
    assert created.status_code == 201
    currency_id = created.json()["id"]

    listed = client.get("/currencies", params={"limit": 100})
    assert listed.status_code == 200
    assert any(c["id"] == currency_id for c in listed.json())

    updated = client.patch(f"/currencies/{currency_id}", json={"decimal_digits": 3})
    assert updated.status_code == 200
    assert updated.json()["decimal_digits"] == 3

    deleted = client.delete(f"/currencies/{currency_id}")
    assert deleted.status_code == 204


def test_credential_fields_never_appear_in_create_or_get_response(client):
    created = client.post(
        "/users",
        json={
            "name": "API Coverage User",
            "username": "coverage",
            "password": "p4ss!",
            "api_key": "k3y!",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert "password" not in body
    assert "api_key" not in body

    fetched = client.get(f"/users/{body['id']}")
    assert "password" not in fetched.json()
    assert "api_key" not in fetched.json()


def test_status_operation_enables_and_disables(client):
    created = client.post(
        "/trading-platforms", json={"name": "Status Platform", "code": "status_platform"}
    )
    platform_id = created.json()["id"]

    disabled = client.post(f"/trading-platforms/{platform_id}/status", json={"action": "disable"})
    assert disabled.status_code == 200
    assert disabled.json()["status"] is False

    enabled = client.post(f"/trading-platforms/{platform_id}/status", json={"action": "enable"})
    assert enabled.json()["status"] is True


def test_status_operation_rejects_an_invalid_action(client):
    created = client.post(
        "/trading-platforms", json={"name": "Bad Action Platform", "code": "bad_action"}
    )
    platform_id = created.json()["id"]

    response = client.post(f"/trading-platforms/{platform_id}/status", json={"action": "bogus"})
    assert response.status_code == 422


def test_not_found_maps_to_404(client):
    assert client.get("/brokers/999999").status_code == 404


def test_validation_failure_maps_to_422(client):
    response = client.post("/brokers", json={"name": "", "user_id": 1})
    assert response.status_code == 422


def test_duplicate_unique_value_maps_to_409(client):
    response = client.post(
        "/users", json={"name": "Admin", "username": "dupe", "password": "x", "api_key": "y"}
    )
    assert response.status_code == 409


def test_delete_of_referenced_record_maps_to_409(client):
    (currency,) = [
        c for c in client.get("/currencies", params={"limit": 100}).json() if c["code"] == "USD"
    ]
    response = client.delete(f"/currencies/{currency['id']}")
    assert response.status_code == 409
