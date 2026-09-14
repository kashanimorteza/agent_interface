"""Tests for the Action Domain Definition (task P1-G6-T2)."""

from __future__ import annotations

from decimal import Decimal

from model import Action


def _make() -> Action:
    return Action(
        name="Default",
        action_group_id=1,
        asset_id=1,
        account_id=1,
        partial_group_id=1,
        trailing_group_id=1,
        risk_by_reward=Decimal("1"),
        take_profit=Decimal("1"),
        stop_loss=Decimal("1"),
    )


def test_exact_field_set() -> None:
    assert set(Action.model_fields) == {
        "id",
        "name",
        "action_group_id",
        "asset_id",
        "account_id",
        "partial_group_id",
        "trailing_group_id",
        "risk_by_reward",
        "take_profit",
        "stop_loss",
        "is_active",
        "description",
    }


def test_uniqueness_on_action_group_and_name() -> None:
    assert Action.UNIQUE_CONSTRAINTS == (("action_group_id", "name"),)


def test_defaults() -> None:
    action = _make()
    assert action.is_active is True


def test_json_round_trip_and_schema() -> None:
    action = _make()
    restored = Action.model_validate_json(action.model_dump_json())
    assert restored == action
    assert Action.model_json_schema()["properties"]
