from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from my_model.partial_rule import PartialRule


def test_valid_construction_succeeds() -> None:
    instance = PartialRule(
        name="Rule-1",
        partial_group_id=1,
        profit_percentage=Decimal(50),
        close_percentage=Decimal(25),
    )
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        PartialRule(name="Rule-1", partial_group_id=1, profit_percentage=Decimal(50))  # pyright: ignore[reportCallIssue] - deliberately missing close_percentage


def test_uniqueness_rules_are_declared() -> None:
    assert PartialRule.UNIQUE_TOGETHER == (
        ("name",),
        ("partial_group_id", "profit_percentage"),
    )
