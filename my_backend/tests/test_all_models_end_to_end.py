"""Creates one record of every one of the fifteen Models through the live API,
in dependency order, proving every router/Logic unit genuinely works end to end."""

from __future__ import annotations

from datetime import UTC, datetime


def test_create_one_of_every_model_through_the_api(client):
    user = client.post(
        "/users",
        json={"name": "Ada", "username": "ada", "password": "x", "api_key": "y"},
    ).json()

    platform = client.post(
        "/trading-platforms", json={"name": "MetaTrader 5", "code": "metatrader_5"}
    ).json()

    currency = client.post(
        "/currencies", json={"user_id": user["id"], "code": "USD"}
    ).json()

    broker = client.post(
        "/brokers", json={"name": "FxPro", "user_id": user["id"]}
    ).json()

    instance = client.post(
        "/instances",
        json={
            "user_id": user["id"],
            "name": "MT",
            "trading_platform_id": platform["id"],
        },
    ).json()

    asset = client.post(
        "/assets",
        json={"broker_id": broker["id"], "symbol": "EUR/USD", "category": "Currency"},
    ).json()

    account_group = client.post(
        "/account-groups", json={"user_id": user["id"], "name": "Default"}
    ).json()

    account = client.post(
        "/accounts",
        json={
            "name": "Acc-1",
            "group_id": account_group["id"],
            "broker_id": broker["id"],
            "instance_id": instance["id"],
            "base_currency_id": currency["id"],
            "username": "test",
            "password": "secret",
            "leverage": 100,
            "account_type": "CFD",
        },
    ).json()

    trailing_group = client.post(
        "/trailing-groups", json={"user_id": user["id"], "name": "Default"}
    ).json()

    trailing_rule = client.post(
        "/trailing-rules",
        json={
            "name": "TR-1",
            "trailing_group_id": trailing_group["id"],
            "trigger_percentage": "50",
        },
    ).json()

    partial_group = client.post(
        "/partial-groups", json={"user_id": user["id"], "name": "Default"}
    ).json()

    partial_rule = client.post(
        "/partial-rules",
        json={
            "name": "PR-1",
            "partial_group_id": partial_group["id"],
            "profit_percentage": "50",
            "close_percentage": "25",
        },
    ).json()

    action_group = client.post(
        "/action-groups", json={"user_id": user["id"], "name": "Default"}
    ).json()

    action = client.post(
        "/actions",
        json={
            "name": "Default",
            "action_group_id": action_group["id"],
            "asset_id": asset["id"],
            "account_id": account["id"],
            "partial_group_id": partial_group["id"],
            "trailing_group_id": trailing_group["id"],
            "risk_by_reward": "1",
            "take_profit": "1",
            "stop_loss": "1",
        },
    ).json()

    position = client.post(
        "/positions",
        json={
            "user_id": user["id"],
            "name": "Pos-1",
            "trading_platform_id": platform["id"],
            "broker_id": broker["id"],
            "account_id": account["id"],
            "trailing_group_id": trailing_group["id"],
            "partial_group_id": partial_group["id"],
            "action_group_id": action_group["id"],
            "action_id": action["id"],
            "date": datetime.now(UTC).isoformat(),
            "volume": "1",
            "order_type": "market",
            "base_tp": "1",
            "base_sl": "1",
            "real_tp": "1",
            "real_sl": "1",
        },
    )

    assert position.status_code == 201, position.text
    for created in (
        user,
        platform,
        currency,
        broker,
        instance,
        asset,
        account_group,
        account,
        trailing_group,
        trailing_rule,
        partial_group,
        partial_rule,
        action_group,
        action,
    ):
        assert "id" in created and created["id"] is not None
