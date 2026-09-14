"""Verifies the Trailing Rule Domain Definition (Task P1-G5-T2)."""

from __future__ import annotations

from decimal import Decimal

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import TrailingRule

EXPECTED_FIELDS = {
    "id": True,
    "name": True,
    "trailing_group_id": True,
    "trigger_percentage": True,
    "take_profit_adjustment": False,
    "stop_loss_adjustment": False,
    "status": False,
    "description": False,
}


def _make(**overrides):
    kwargs = {
        "id": 1,
        "name": "R1",
        "trailing_group_id": 1,
        "trigger_percentage": Decimal(50),
    }
    kwargs.update(overrides)
    return TrailingRule(**kwargs)


def test_matches_target_definition() -> None:
    assert_exact_fields(TrailingRule, EXPECTED_FIELDS)
    assert_credential_fields(TrailingRule, ())
    assert_unique_constraints(
        TrailingRule, (("name",), ("trailing_group_id", "trigger_percentage"))
    )


def test_defaults() -> None:
    rule = _make()
    assert rule.take_profit_adjustment is None
    assert rule.stop_loss_adjustment is None
    assert rule.status is True


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        TrailingRule(id=1, name="R1", trailing_group_id=1)  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    rule = _make(
        take_profit_adjustment=Decimal("1.5"), stop_loss_adjustment=Decimal("0.5")
    )
    assert TrailingRule.model_validate_json(rule.model_dump_json()) == rule
    assert set(EXPECTED_FIELDS) <= set(TrailingRule.model_json_schema()["properties"])
