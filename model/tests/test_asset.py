"""Verifies P1T7: the Asset Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Asset

VALID = {
    "id": 1,
    "broker_id": 1,
    "symbol": "EUR/USD",
    "category": "Currency",
    "point_size": 0.0001,
    "digits": 5,
}


@pytest.mark.parametrize("omit", ["broker_id", "symbol", "category"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        Asset(**payload)


def test_valid_asset_round_trips_preserving_defaults() -> None:
    asset = Asset(**VALID)
    restored = Asset(**asset.model_dump())
    assert restored == asset
    minimal = Asset(id=2, broker_id=1, symbol="USOil", category="Commodity")
    assert minimal.point_size == 0.0
    assert minimal.digits == 0


def test_published_metadata_declares_composite_unique() -> None:
    meta = Asset.persistence_metadata()
    assert meta["unique_sets"] == [["broker_id", "symbol"]]
    assert meta["fields"]["broker_id"]["foreign_key"] == "broker.id"
