"""Verifies P1T15: the Action Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Action

VALID = {
    "id": 1,
    "name": "Default",
    "action_group_id": 1,
    "asset_id": 1,
    "account_id": 1,
    "partial_group_id": 1,
    "trailing_group_id": 1,
    "risk_by_reward": "1",
    "take_profit": "1",
    "stop_loss": "1",
}


@pytest.mark.parametrize(
    "omit",
    [
        "name",
        "action_group_id",
        "asset_id",
        "account_id",
        "partial_group_id",
        "trailing_group_id",
        "risk_by_reward",
        "take_profit",
        "stop_loss",
    ],
)
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        Action(**payload)


def test_valid_action_round_trips_preserving_five_relationships() -> None:
    action = Action(**VALID)
    restored = Action(**action.model_dump())
    assert restored == action
    for field in (
        "action_group_id",
        "asset_id",
        "account_id",
        "partial_group_id",
        "trailing_group_id",
    ):
        assert getattr(restored, field) == 1


def test_published_metadata_declares_composite_unique() -> None:
    meta = Action.persistence_metadata()
    assert meta["unique_sets"] == [["action_group_id", "name"]]
