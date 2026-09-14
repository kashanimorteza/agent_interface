"""Tests for Financial Reference Model Logic (tasks P3-G5-T1..T3)."""

from __future__ import annotations

from backend.database_interface import DatabaseInterface
from backend.logic.asset import AssetLogic
from backend.logic.broker import BrokerLogic
from backend.logic.currency import CurrencyLogic
from backend.logic.user import UserLogic


def _di(db) -> DatabaseInterface:
    return DatabaseInterface(db, timeout_seconds=5.0, max_retry_attempts=3)


def _user(di):
    return UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"}
    )


def test_currency_logic_exposes_standard_operations(db) -> None:
    di = _di(db)
    user = _user(di)
    logic = CurrencyLogic(di)
    currency = logic.create({"user_id": user.id, "code": "USD"})
    assert logic.get_by_id(currency.id).code == "USD"
    assert logic.update(currency.id, {"symbol": "$"}).symbol == "$"
    assert logic.disable(currency.id).is_active is False


def test_broker_logic_exposes_standard_operations(db) -> None:
    di = _di(db)
    user = _user(di)
    logic = BrokerLogic(di)
    broker = logic.create({"name": "FxPro", "user_id": user.id})
    assert logic.get_by_id(broker.id).name == "FxPro"
    assert broker in logic.list()


def test_asset_logic_validates_broker_relationship(db) -> None:
    di = _di(db)
    user = _user(di)
    broker = BrokerLogic(di).create({"name": "FxPro", "user_id": user.id})
    logic = AssetLogic(di)
    asset = logic.create({"broker_id": broker.id, "symbol": "EUR/USD", "category": "Currency"})
    assert logic.get_by_id(asset.id).broker_id == broker.id
