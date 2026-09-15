"""Verifies P1T13: the Partial Rule Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import PartialRule

VALID = {
    "id": 1,
    "name": "Rule-1",
    "partial_group_id": 1,
    "profit_percentage": "50",
    "close_percentage": "25",
}


@pytest.mark.parametrize(
    "omit", ["name", "partial_group_id", "profit_percentage", "close_percentage"]
)
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        PartialRule(**payload)


def test_valid_partial_rule_round_trips_preserving_reference() -> None:
    rule = PartialRule(**VALID)
    restored = PartialRule(**rule.model_dump())
    assert restored == rule


def test_published_metadata_declares_unique_and_composite_unique() -> None:
    meta = PartialRule.persistence_metadata()
    assert meta["fields"]["name"]["unique"] is True
    assert meta["unique_sets"] == [["partial_group_id", "profit_percentage"]]
