"""Generic Model-driven HTTP operations: create, get, list, update, delete,
status, and their distinguishable failure outcomes.
"""

from fastapi.testclient import TestClient


def _create_user(client: TestClient, **overrides: object) -> dict:
    payload: dict[str, object] = {"name": "Admin", "username": "admin", "password": "x", "api_key": "y"}
    payload.update(overrides)
    return client.post("/users", json=payload).json()


def test_create_returns_201_and_excludes_credentials(client: TestClient) -> None:
    response = client.post(
        "/users", json={"name": "Admin", "username": "admin", "password": "x", "api_key": "y"}
    )
    assert response.status_code == 201
    body = response.json()
    assert "password" not in body
    assert "api_key" not in body
    assert body["status"] is True


def test_get_returns_the_created_record(client: TestClient) -> None:
    created = _create_user(client)
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Admin"


def test_get_missing_identifier_returns_404(client: TestClient) -> None:
    response = client.get("/users/999999")
    assert response.status_code == 404


def test_list_returns_every_created_record(client: TestClient) -> None:
    _create_user(client, name="First", username="first")
    _create_user(client, name="Second", username="second")
    response = client.get("/users")
    assert response.status_code == 200
    assert {record["name"] for record in response.json()} == {"First", "Second"}


def test_update_preserves_omitted_fields_and_replaces_supplied_ones(client: TestClient) -> None:
    created = _create_user(client, description="original")
    response = client.patch(f"/users/{created['id']}", json={"description": "updated"})
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "updated"
    assert body["name"] == "Admin"  # omitted from the patch: unchanged


def test_update_missing_identifier_returns_404(client: TestClient) -> None:
    response = client.patch("/users/999999", json={"description": "x"})
    assert response.status_code == 404


def test_delete_then_get_returns_404(client: TestClient) -> None:
    created = _create_user(client)
    delete_response = client.delete(f"/users/{created['id']}")
    assert delete_response.status_code == 204
    assert client.get(f"/users/{created['id']}").status_code == 404


def test_status_enable_and_disable(client: TestClient) -> None:
    created = _create_user(client)
    disabled = client.post(f"/users/{created['id']}/status", json={"action": "disable"})
    assert disabled.status_code == 200
    assert disabled.json()["status"] is False
    enabled = client.post(f"/users/{created['id']}/status", json={"action": "enable"})
    assert enabled.json()["status"] is True


def test_uniqueness_violation_returns_409(client: TestClient) -> None:
    _create_user(client, name="Admin")
    response = client.post(
        "/users", json={"name": "Admin", "username": "different", "password": "x", "api_key": "y"}
    )
    assert response.status_code == 409


def test_validation_failure_returns_422(client: TestClient) -> None:
    response = client.post("/currencies", json={"user_id": 1, "code": "US"})
    assert response.status_code == 422


def test_a_model_without_credentials_round_trips_normally(client: TestClient) -> None:
    response = client.post("/trading-platforms", json={"name": "MT5", "code": "metatrader_5"})
    assert response.status_code == 201
    assert response.json()["code"] == "metatrader_5"
