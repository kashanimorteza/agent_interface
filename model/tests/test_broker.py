"""Verifies P1T6: the Broker Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Broker

VALID = {"id": 1, "name": "FxPro", "user_id": 1}


@pytest.mark.parametrize("omit", ["name", "user_id"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        Broker(**payload)


def test_valid_broker_round_trips_through_serialization() -> None:
    broker = Broker(**VALID)
    restored = Broker(**broker.model_dump())
    assert restored == broker


def test_published_metadata_declares_composite_unique() -> None:
    meta = Broker.persistence_metadata()
    assert meta["unique_sets"] == [["user_id", "name"]]
