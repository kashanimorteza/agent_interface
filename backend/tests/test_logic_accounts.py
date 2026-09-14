"""Tests for Accounts Model Logic (tasks P3-G6-T1..T2)."""

from __future__ import annotations

from backend.database_interface import DatabaseInterface
from backend.logic.account import AccountLogic
from backend.logic.account_group import AccountGroupLogic
from backend.logic.broker import BrokerLogic
from backend.logic.currency import CurrencyLogic
from backend.logic.instance import InstanceLogic
from backend.logic.trading_platform import TradingPlatformLogic
from backend.logic.user import UserLogic


def _di(db) -> DatabaseInterface:
    return DatabaseInterface(db, timeout_seconds=5.0, max_retry_attempts=3)


def test_account_group_logic_exposes_standard_operations(db) -> None:
    di = _di(db)
    user = UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"}
    )
    logic = AccountGroupLogic(di)
    group = logic.create({"user_id": user.id, "name": "Default"})
    assert logic.get_by_id(group.id).name == "Default"


def test_account_logic_validates_relationships_and_redacts_credential(db) -> None:
    di = _di(db)
    user = UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"}
    )
    platform = TradingPlatformLogic(di).create({"name": "MetaTrader 5", "code": "metatrader_5"})
    instance = InstanceLogic(di).create(
        {"user_id": user.id, "name": "MetaTrader", "trading_platform_id": platform.id}
    )
    broker = BrokerLogic(di).create({"name": "FxPro", "user_id": user.id})
    currency = CurrencyLogic(di).create({"user_id": user.id, "code": "USD"})
    group = AccountGroupLogic(di).create({"user_id": user.id, "name": "Default"})

    logic = AccountLogic(di)
    account = logic.create(
        {
            "name": "Acc-1",
            "group_id": group.id,
            "broker_id": broker.id,
            "instance_id": instance.id,
            "base_currency_id": currency.id,
            "username": "test",
            "password": "secret",
            "leverage": 100,
            "account_type": "CFD",
        }
    )
    assert account.password != "secret"
    assert logic.get_by_id(account.id).group_id == group.id
