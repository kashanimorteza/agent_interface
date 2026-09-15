"""Verifies the id field of every Domain Definition follows Target's 'Auto Increment: true'
declaration as a generated field: constructible without a value, while its published
storage metadata still marks it non-nullable (Model Principle 6).

This corrects Finding P1F4, raised during Phase 2 (Database) development: id fields
were previously required with no default, making it impossible to construct a
not-yet-persisted Domain Definition.
"""

from __future__ import annotations

from model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    PartialRule,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)

MINIMAL_FIELDS = {
    User: {"name": "n", "username": "u", "password": "p", "api_key": "k"},
    TradingPlatform: {"name": "n", "code": "c"},
    Instance: {"user_id": 1, "trading_platform_id": 1, "name": "n"},
    Currency: {"user_id": 1, "code": "USD"},
    Broker: {"name": "n", "user_id": 1},
    Asset: {"broker_id": 1, "symbol": "s", "category": "c"},
    AccountGroup: {"user_id": 1, "name": "n"},
    Account: {
        "name": "n",
        "group_id": 1,
        "broker_id": 1,
        "instance_id": 1,
        "base_currency_id": 1,
        "username": "u",
        "password": "p",
        "leverage": 1,
        "account_type": "t",
    },
    TrailingGroup: {"user_id": 1, "name": "n"},
    TrailingRule: {"name": "n", "trailing_group_id": 1, "trigger_percentage": "1"},
    PartialGroup: {"user_id": 1, "name": "n"},
    PartialRule: {
        "name": "n",
        "partial_group_id": 1,
        "profit_percentage": "1",
        "close_percentage": "1",
    },
    ActionGroup: {"user_id": 1, "name": "n"},
    Action: {
        "name": "n",
        "action_group_id": 1,
        "asset_id": 1,
        "account_id": 1,
        "partial_group_id": 1,
        "trailing_group_id": 1,
        "risk_by_reward": "1",
        "take_profit": "1",
        "stop_loss": "1",
    },
}


def test_id_is_constructible_without_a_value_for_every_persistent_model() -> None:
    for model_cls, fields in MINIMAL_FIELDS.items():
        instance = model_cls(**fields)
        assert instance.id is None, (
            f"{model_cls.__name__}.id should default to None when omitted"
        )


def test_published_id_metadata_still_declares_non_nullable_primary_key() -> None:
    for model_cls in MINIMAL_FIELDS:
        meta = model_cls.persistence_metadata()["fields"]["id"]
        assert meta["nullable"] is False
        assert meta["primary_key"] is True
        assert meta["auto_increment"] is True


def test_explicit_id_is_still_preserved_when_provided() -> None:
    user = User(id=42, name="n", username="u", password="p", api_key="k")
    assert user.id == 42
