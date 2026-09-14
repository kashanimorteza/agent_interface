"""Tests for Actions and Positions Model Logic (tasks P3-G8-T1..T3)."""

from __future__ import annotations

import datetime
from decimal import Decimal

from backend.database_interface import DatabaseInterface
from backend.logic.account import AccountLogic
from backend.logic.account_group import AccountGroupLogic
from backend.logic.action import ActionLogic
from backend.logic.action_group import ActionGroupLogic
from backend.logic.asset import AssetLogic
from backend.logic.broker import BrokerLogic
from backend.logic.currency import CurrencyLogic
from backend.logic.instance import InstanceLogic
from backend.logic.partial_group import PartialGroupLogic
from backend.logic.position import PositionLogic
from backend.logic.trading_platform import TradingPlatformLogic
from backend.logic.trailing_group import TrailingGroupLogic
from backend.logic.user import UserLogic


def _di(db) -> DatabaseInterface:
    return DatabaseInterface(db, timeout_seconds=5.0, max_retry_attempts=3)


def _build_chain(di):
    user = UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"}
    )
    platform = TradingPlatformLogic(di).create({"name": "MetaTrader 5", "code": "metatrader_5"})
    instance = InstanceLogic(di).create(
        {"user_id": user.id, "name": "MetaTrader", "trading_platform_id": platform.id}
    )
    broker = BrokerLogic(di).create({"name": "FxPro", "user_id": user.id})
    currency = CurrencyLogic(di).create({"user_id": user.id, "code": "USD"})
    asset = AssetLogic(di).create(
        {"broker_id": broker.id, "symbol": "EUR/USD", "category": "Currency"}
    )
    account_group = AccountGroupLogic(di).create({"user_id": user.id, "name": "Default"})
    account = AccountLogic(di).create(
        {
            "name": "Acc-1",
            "group_id": account_group.id,
            "broker_id": broker.id,
            "instance_id": instance.id,
            "base_currency_id": currency.id,
            "username": "test",
            "password": "secret",
            "leverage": 100,
            "account_type": "CFD",
        }
    )
    partial_group = PartialGroupLogic(di).create({"user_id": user.id, "name": "Default"})
    trailing_group = TrailingGroupLogic(di).create({"user_id": user.id, "name": "Default"})
    action_group = ActionGroupLogic(di).create({"user_id": user.id, "name": "Default"})
    return {
        "user": user,
        "platform": platform,
        "broker": broker,
        "asset": asset,
        "account": account,
        "partial_group": partial_group,
        "trailing_group": trailing_group,
        "action_group": action_group,
    }


def test_action_group_and_action_logic(db) -> None:
    di = _di(db)
    chain = _build_chain(di)
    logic = ActionLogic(di)
    action = logic.create(
        {
            "name": "Default",
            "action_group_id": chain["action_group"].id,
            "asset_id": chain["asset"].id,
            "account_id": chain["account"].id,
            "partial_group_id": chain["partial_group"].id,
            "trailing_group_id": chain["trailing_group"].id,
            "risk_by_reward": Decimal("1"),
            "take_profit": Decimal("1"),
            "stop_loss": Decimal("1"),
        }
    )
    assert logic.get_by_id(action.id).action_group_id == chain["action_group"].id


def test_position_logic_validates_full_relationship_set(db) -> None:
    di = _di(db)
    chain = _build_chain(di)
    action = ActionLogic(di).create(
        {
            "name": "Default",
            "action_group_id": chain["action_group"].id,
            "asset_id": chain["asset"].id,
            "account_id": chain["account"].id,
            "partial_group_id": chain["partial_group"].id,
            "trailing_group_id": chain["trailing_group"].id,
            "risk_by_reward": Decimal("1"),
            "take_profit": Decimal("1"),
            "stop_loss": Decimal("1"),
        }
    )
    logic = PositionLogic(di)
    position = logic.create(
        {
            "user_id": chain["user"].id,
            "name": "Pos-1",
            "trading_platform_id": chain["platform"].id,
            "broker_id": chain["broker"].id,
            "account_id": chain["account"].id,
            "trailing_group_id": chain["trailing_group"].id,
            "partial_group_id": chain["partial_group"].id,
            "action_group_id": chain["action_group"].id,
            "action_id": action.id,
            "date": datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
            "volume": Decimal("1"),
            "order_type": "market",
            "base_tp": Decimal("1"),
            "base_sl": Decimal("1"),
            "real_tp": Decimal("1"),
            "real_sl": Decimal("1"),
        }
    )
    assert logic.get_by_id(position.id).action_id == action.id
