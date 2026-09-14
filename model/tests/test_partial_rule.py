"""Tests for the Partial Rule Domain Definition (task P1-G5-T4)."""

from __future__ import annotations

from decimal import Decimal

from model import PartialRule


def _make() -> PartialRule:
    return PartialRule(
        name="Rule-1",
        partial_group_id=1,
        profit_percentage=Decimal("25"),
        close_percentage=Decimal("50"),
    )


def test_exact_field_set() -> None:
    assert set(PartialRule.model_fields) == {
        "id",
        "name",
        "partial_group_id",
        "profit_percentage",
        "close_percentage",
        "is_active",
        "description",
    }


def test_both_uniqueness_groups() -> None:
    assert PartialRule.UNIQUE_CONSTRAINTS == (
        ("name",),
        ("partial_group_id", "profit_percentage"),
    )


def test_defaults() -> None:
    rule = _make()
    assert rule.is_active is True


def test_json_round_trip_and_schema() -> None:
    rule = _make()
    restored = PartialRule.model_validate_json(rule.model_dump_json())
    assert restored == rule
    assert PartialRule.model_json_schema()["properties"]
