"""Tests for Identity and Connectivity Model Logic (tasks P3-G4-T1..T3)."""

from __future__ import annotations

from backend.database_interface import DatabaseInterface
from backend.logic.instance import InstanceLogic
from backend.logic.trading_platform import TradingPlatformLogic
from backend.logic.user import UserLogic


def _di(db) -> DatabaseInterface:
    return DatabaseInterface(db, timeout_seconds=5.0, max_retry_attempts=3)


def test_user_logic_exposes_standard_operations_and_redacts_credentials(db) -> None:
    logic = UserLogic(_di(db))
    user = logic.create({"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"})
    assert user.password != "pw"
    assert user.api_key != "key"

    fetched = logic.get_by_id(user.id)
    assert fetched.password != "pw"

    updated = logic.update(user.id, {"description": "engineer"})
    assert updated.description == "engineer"

    assert logic.disable(user.id).is_active is False
    assert logic.enable(user.id).is_active is True
    assert not hasattr(logic, "delete")


def test_trading_platform_logic_exposes_standard_operations(db) -> None:
    logic = TradingPlatformLogic(_di(db))
    platform = logic.create({"name": "MetaTrader 5", "code": "metatrader_5"})
    assert logic.get_by_id(platform.id).code == "metatrader_5"
    assert platform in logic.list()
    assert logic.update(platform.id, {"description": "primary"}).description == "primary"
    assert not hasattr(logic, "delete")


def test_instance_logic_validates_relationships_and_redacts_credentials(db) -> None:
    di = _di(db)
    user = UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"}
    )
    platform = TradingPlatformLogic(di).create({"name": "MetaTrader 5", "code": "metatrader_5"})

    logic = InstanceLogic(di)
    instance = logic.create(
        {
            "user_id": user.id,
            "name": "MetaTrader",
            "trading_platform_id": platform.id,
            "password": "secret",
            "api_key": "secret-key",
        }
    )
    assert instance.user_id == user.id
    assert instance.password != "secret"
    assert instance.api_key != "secret-key"
    assert not hasattr(logic, "delete")
