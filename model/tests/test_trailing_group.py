"""Verifies P1T10: the Trailing Group Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import TrailingGroup

VALID = {"id": 1, "user_id": 1, "name": "Default"}


@pytest.mark.parametrize("omit", ["user_id", "name"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        TrailingGroup(**payload)


def test_valid_trailing_group_round_trips_through_serialization() -> None:
    group = TrailingGroup(**VALID)
    restored = TrailingGroup(**group.model_dump())
    assert restored == group


def test_published_metadata_declares_composite_unique() -> None:
    meta = TrailingGroup.persistence_metadata()
    assert meta["unique_sets"] == [["user_id", "name"]]
