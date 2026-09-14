"""Tests for the Trading Platform Domain Definition (task P1-G2-T2)."""

from __future__ import annotations

from model import TradingPlatform


def _make() -> TradingPlatform:
    return TradingPlatform(name="MetaTrader 5", code="metatrader_5")


def test_exact_field_set() -> None:
    assert set(TradingPlatform.model_fields) == {
        "id",
        "name",
        "code",
        "is_active",
        "description",
    }


def test_no_credential_fields() -> None:
    assert all(field.json_schema_extra is None for field in TradingPlatform.model_fields.values())


def test_no_uniqueness_declared() -> None:
    assert TradingPlatform.UNIQUE_CONSTRAINTS == ()


def test_defaults() -> None:
    platform = _make()
    assert platform.is_active is True
    assert platform.description is None


def test_json_round_trip_and_schema() -> None:
    platform = _make()
    restored = TradingPlatform.model_validate_json(platform.model_dump_json())
    assert restored == platform
    assert TradingPlatform.model_json_schema()["properties"]
