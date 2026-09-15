"""Verifies P1T14: the Action Group Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import ActionGroup

VALID = {"id": 1, "user_id": 1, "name": "Default"}


@pytest.mark.parametrize("omit", ["user_id", "name"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        ActionGroup(**payload)


def test_valid_action_group_round_trips_through_serialization() -> None:
    group = ActionGroup(**VALID)
    restored = ActionGroup(**group.model_dump())
    assert restored == group


def test_published_metadata_declares_composite_unique() -> None:
    meta = ActionGroup.persistence_metadata()
    assert meta["unique_sets"] == [["user_id", "name"]]
