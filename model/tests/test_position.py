"""Verifies P1T16: the Position Domain Definition."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from model import Position

VALID = {
    "id": 1,
    "user_id": 1,
    "name": "Pos-1",
    "trading_platform_id": 1,
    "broker_id": 1,
    "account_id": 1,
    "trailing_group_id": 1,
    "partial_group_id": 1,
    "action_group_id": 1,
    "action_id": 1,
    "date": datetime(2026, 1, 1, tzinfo=UTC),
    "volume": "1.0",
    "order_type": "market",
    "base_tp": "1",
    "base_sl": "1",
    "real_tp": "1",
    "real_sl": "1",
}


@pytest.mark.parametrize(
    "omit",
    [
        "user_id",
        "name",
        "trading_platform_id",
        "broker_id",
        "account_id",
        "trailing_group_id",
        "partial_group_id",
        "action_group_id",
        "action_id",
        "date",
        "volume",
        "order_type",
        "base_tp",
        "base_sl",
        "real_tp",
        "real_sl",
    ],
)
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        Position(**payload)


def test_naive_datetime_is_rejected() -> None:
    naive_date = datetime.now().replace(tzinfo=None)  # noqa: DTZ005 - intentionally naive
    payload = {**VALID, "date": naive_date}
    with pytest.raises(ValidationError):
        Position(**payload)


def test_valid_position_round_trips_preserving_eight_relationships_and_defaults() -> (
    None
):
    position = Position(**VALID)
    restored = Position(**position.model_dump())
    assert restored == position
    assert restored.profit == 0
    assert restored.is_executed is False
    for field in (
        "user_id",
        "trading_platform_id",
        "broker_id",
        "account_id",
        "trailing_group_id",
        "partial_group_id",
        "action_group_id",
        "action_id",
    ):
        assert getattr(restored, field) == 1


def test_published_metadata_declares_name_as_unique() -> None:
    meta = Position.persistence_metadata()
    assert meta["fields"]["name"]["unique"] is True
