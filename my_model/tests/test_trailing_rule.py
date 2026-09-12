from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from my_model.trailing_rule import TrailingRule


def test_valid_construction_succeeds() -> None:
    instance = TrailingRule(
        name="Rule-1", trailing_group_id=1, trigger_percentage=Decimal(50)
    )
    assert instance.status is True
    assert instance.take_profit_adjustment is None


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        TrailingRule(name="Rule-1", trailing_group_id=1)  # pyright: ignore[reportCallIssue] - deliberately missing trigger_percentage


def test_uniqueness_rules_are_declared() -> None:
    assert TrailingRule.UNIQUE_TOGETHER == (
        ("name",),
        ("trailing_group_id", "trigger_percentage"),
    )
