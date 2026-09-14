"""Tests for the Trailing Rule Domain Definition (task P1-G5-T2)."""

from __future__ import annotations

from decimal import Decimal

from model import TrailingRule


def _make() -> TrailingRule:
    return TrailingRule(name="Rule-1", trailing_group_id=1, trigger_percentage=Decimal("50"))


def test_exact_field_set() -> None:
    assert set(TrailingRule.model_fields) == {
        "id",
        "name",
        "trailing_group_id",
        "trigger_percentage",
        "take_profit_adjustment",
        "stop_loss_adjustment",
        "is_active",
        "description",
    }


def test_both_uniqueness_groups() -> None:
    assert TrailingRule.UNIQUE_CONSTRAINTS == (
        ("name",),
        ("trailing_group_id", "trigger_percentage"),
    )


def test_nullable_defaults() -> None:
    rule = _make()
    assert rule.take_profit_adjustment is None
    assert rule.stop_loss_adjustment is None


def test_json_round_trip_and_schema() -> None:
    rule = _make()
    restored = TrailingRule.model_validate_json(rule.model_dump_json())
    assert restored == rule
    assert TrailingRule.model_json_schema()["properties"]
