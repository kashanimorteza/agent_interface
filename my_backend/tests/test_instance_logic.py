"""The Target-declared rule that the selected Trading Platform determines
which Instance connection fields are required — Backend Logic's own
responsibility, since neither Model nor Database enforces it.
"""

from fastapi.testclient import TestClient


def _setup(client: TestClient) -> tuple[int, int, int]:
    user = client.post(
        "/users", json={"name": "U1", "username": "u1", "password": "x", "api_key": "y"}
    ).json()
    mt5 = client.post("/trading-platforms", json={"name": "MetaTrader 5", "code": "metatrader_5"}).json()
    binance = client.post("/trading-platforms", json={"name": "Binance", "code": "binance"}).json()
    return user["id"], mt5["id"], binance["id"]


def test_missing_platform_required_field_is_rejected(client: TestClient) -> None:
    user_id, mt5_id, _binance_id = _setup(client)
    response = client.post(
        "/instances",
        json={
            "user_id": user_id,
            "name": "MT-bad",
            "trading_platform_id": mt5_id,
            "ip": "1.2.3.4",
            "username": "u",
            # password omitted: MetaTrader 5 requires it
        },
    )
    assert response.status_code == 422


def test_instance_with_every_platform_required_field_succeeds(client: TestClient) -> None:
    user_id, mt5_id, _binance_id = _setup(client)
    response = client.post(
        "/instances",
        json={
            "user_id": user_id,
            "name": "MT-good",
            "trading_platform_id": mt5_id,
            "ip": "1.2.3.4",
            "username": "u",
            "password": "p",
        },
    )
    assert response.status_code == 201


def test_a_different_platform_has_different_required_fields(client: TestClient) -> None:
    user_id, _mt5_id, binance_id = _setup(client)
    response = client.post(
        "/instances",
        json={"user_id": user_id, "name": "BN-good", "trading_platform_id": binance_id, "api_key": "k"},
    )
    assert response.status_code == 201


def test_update_re_validates_the_platform_requirement(client: TestClient) -> None:
    user_id, mt5_id, binance_id = _setup(client)
    created = client.post(
        "/instances",
        json={"user_id": user_id, "name": "BN-good", "trading_platform_id": binance_id, "api_key": "k"},
    ).json()

    # Switching to MetaTrader 5 without supplying its required fields must be rejected.
    response = client.patch(f"/instances/{created['id']}", json={"trading_platform_id": mt5_id})
    assert response.status_code == 422
