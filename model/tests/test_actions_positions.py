"""Tests for Action Group, Action, and Position."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from model.action import Action
from model.action_group import ActionGroup
from model.foundation import ForeignKey, persistence_contract
from model.position import Position


def test_action_group_relationship_and_uniqueness() -> None:
    group = ActionGroup(user_id=1, name="Default")
    assert group.is_active is True
    contract = persistence_contract(ActionGroup)
    assert contract.unique_sets == (("user_id", "name"),)


def test_action_relationships_and_uniqueness() -> None:
    action = Action(
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
    assert action.is_active is True

    contract = persistence_contract(Action)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["action_group_id"].foreign_key == ForeignKey("ActionGroup", "id")
    assert by_name["asset_id"].foreign_key == ForeignKey("Asset", "id")
    assert by_name["account_id"].foreign_key == ForeignKey("Account", "id")
    assert by_name["partial_group_id"].foreign_key == ForeignKey("PartialGroup", "id")
    assert by_name["trailing_group_id"].foreign_key == ForeignKey("TrailingGroup", "id")
    assert contract.unique_sets == (("action_group_id", "name"),)

    with pytest.raises(ValidationError):
        Action(name="Default", action_group_id=1, asset_id=1)  # type: ignore[call-arg]


def test_position_relationships_and_defaults() -> None:
    position = Position(
        user_id=1,
        name="Pos-1",
        trading_platform_id=1,
        broker_id=1,
        account_id=1,
        trailing_group_id=1,
        partial_group_id=1,
        action_group_id=1,
        action_id=1,
        date=datetime.now(UTC),
        volume=Decimal("1"),
        order_type="market",
        base_tp=Decimal("1"),
        base_sl=Decimal("1"),
        real_tp=Decimal("1"),
        real_sl=Decimal("1"),
    )
    assert position.profit == 0
    assert position.is_executed is False
    assert position.is_active is True

    contract = persistence_contract(Position)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["user_id"].foreign_key == ForeignKey("User", "id")
    assert by_name["trading_platform_id"].foreign_key == ForeignKey("TradingPlatform", "id")
    assert by_name["broker_id"].foreign_key == ForeignKey("Broker", "id")
    assert by_name["account_id"].foreign_key == ForeignKey("Account", "id")
    assert by_name["trailing_group_id"].foreign_key == ForeignKey("TrailingGroup", "id")
    assert by_name["partial_group_id"].foreign_key == ForeignKey("PartialGroup", "id")
    assert by_name["action_group_id"].foreign_key == ForeignKey("ActionGroup", "id")
    assert by_name["action_id"].foreign_key == ForeignKey("Action", "id")
    assert by_name["name"].unique is True

    with pytest.raises(ValidationError):
        Position(
            user_id=1,
            name="Pos-2",
            trading_platform_id=1,
            broker_id=1,
            account_id=1,
            trailing_group_id=1,
            partial_group_id=1,
            action_group_id=1,
            action_id=1,
            date=datetime(2026, 1, 1),  # naive: not timezone-aware
            volume=Decimal("1"),
            order_type="market",
            base_tp=Decimal("1"),
            base_sl=Decimal("1"),
            real_tp=Decimal("1"),
            real_sl=Decimal("1"),
        )
