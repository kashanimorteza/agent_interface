"""Verifies P1T11: the Trailing Rule Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import TrailingRule

VALID = {"id": 1, "name": "Rule-1", "trailing_group_id": 1, "trigger_percentage": "50"}


@pytest.mark.parametrize("omit", ["name", "trailing_group_id", "trigger_percentage"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        TrailingRule(**payload)


def test_valid_trailing_rule_round_trips_preserving_reference() -> None:
    rule = TrailingRule(**VALID)
    restored = TrailingRule(**rule.model_dump())
    assert restored == rule
    assert restored.trailing_group_id == 1


def test_published_metadata_declares_unique_and_composite_unique() -> None:
    meta = TrailingRule.persistence_metadata()
    assert meta["fields"]["name"]["unique"] is True
    assert meta["unique_sets"] == [["trailing_group_id", "trigger_percentage"]]
