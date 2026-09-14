from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from model import Action, ActionGroup, Position


def test_action_group_accepts_valid_data():
    group = ActionGroup(user_id=1, name="Default")
    assert group.is_active is True


def test_action_group_declares_per_user_name_uniqueness_metadata():
    assert ActionGroup.unique_together == (("user_id", "name"),)


def test_action_accepts_valid_data():
    action = Action(
        name="Default",
        action_group_id=1,
        asset_id=1,
        account_id=1,
        partial_group_id=1,
        trailing_group_id=1,
        risk_by_reward=Decimal(1),
        take_profit=Decimal(1),
        stop_loss=Decimal(1),
    )
    assert action.is_active is True


def test_action_declares_per_group_name_uniqueness_metadata():
    assert Action.unique_together == (("action_group_id", "name"),)


def test_position_accepts_valid_data_with_timezone_aware_date():
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
        volume=Decimal(1),
        order_type="market",
        base_tp=Decimal(1),
        base_sl=Decimal(1),
        real_tp=Decimal(1),
        real_sl=Decimal(1),
    )
    assert position.profit == 0
    assert position.is_executed is False


def test_position_rejects_naive_date():
    with pytest.raises(ValidationError):
        Position(
            user_id=1,
            name="Pos-1",
            trading_platform_id=1,
            broker_id=1,
            account_id=1,
            trailing_group_id=1,
            partial_group_id=1,
            action_group_id=1,
            action_id=1,
            date=datetime.now(),  # noqa: DTZ005 (naive datetime is the negative case under test)
            volume=Decimal(1),
            order_type="market",
            base_tp=Decimal(1),
            base_sl=Decimal(1),
            real_tp=Decimal(1),
            real_sl=Decimal(1),
        )


def test_position_declares_display_name_uniqueness_metadata():
    assert Position.unique_together == (("name",),)
