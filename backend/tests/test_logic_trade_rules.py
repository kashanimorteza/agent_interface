"""Tests for Trade Management Rule Model Logic (tasks P3-G7-T1..T4)."""

from __future__ import annotations

from decimal import Decimal

from backend.database_interface import DatabaseInterface
from backend.logic.partial_group import PartialGroupLogic
from backend.logic.partial_rule import PartialRuleLogic
from backend.logic.trailing_group import TrailingGroupLogic
from backend.logic.trailing_rule import TrailingRuleLogic
from backend.logic.user import UserLogic


def _di(db) -> DatabaseInterface:
    return DatabaseInterface(db, timeout_seconds=5.0, max_retry_attempts=3)


def _user(di):
    return UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"}
    )


def test_trailing_group_and_rule_logic(db) -> None:
    di = _di(db)
    user = _user(di)
    group = TrailingGroupLogic(di).create({"user_id": user.id, "name": "Default"})
    rule_logic = TrailingRuleLogic(di)
    rule = rule_logic.create(
        {"name": "Rule-1", "trailing_group_id": group.id, "trigger_percentage": Decimal("50")}
    )
    assert rule_logic.get_by_id(rule.id).trailing_group_id == group.id


def test_partial_group_and_rule_logic(db) -> None:
    di = _di(db)
    user = _user(di)
    group = PartialGroupLogic(di).create({"user_id": user.id, "name": "Default"})
    rule_logic = PartialRuleLogic(di)
    rule = rule_logic.create(
        {
            "name": "Rule-1",
            "partial_group_id": group.id,
            "profit_percentage": Decimal("25"),
            "close_percentage": Decimal("50"),
        }
    )
    assert rule_logic.get_by_id(rule.id).partial_group_id == group.id
