"""Tests for the Asset Domain Definition (task P1-G3-T3)."""

from __future__ import annotations

from model import Asset


def _make() -> Asset:
    return Asset(broker_id=1, symbol="EUR/USD", category="Currency")


def test_exact_field_set() -> None:
    assert set(Asset.model_fields) == {
        "id",
        "broker_id",
        "symbol",
        "category",
        "point_size",
        "digits",
        "is_active",
        "description",
    }


def test_uniqueness_on_broker_and_symbol() -> None:
    assert Asset.UNIQUE_CONSTRAINTS == (("broker_id", "symbol"),)


def test_defaults() -> None:
    asset = _make()
    assert asset.point_size == 0.0
    assert asset.digits == 0
    assert asset.is_active is True


def test_json_round_trip_and_schema() -> None:
    asset = _make()
    restored = Asset.model_validate_json(asset.model_dump_json())
    assert restored == asset
    assert Asset.model_json_schema()["properties"]
