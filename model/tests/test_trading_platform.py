"""Verification for the Trading Platform Domain Definition (Task P1-trading-platform)."""

from __future__ import annotations

from conftest import (
    assert_public_interface,
    assert_rejects_missing_required,
    assert_rejects_null_for_non_nullable,
    assert_rejects_unknown_field,
    assert_rejects_wrong_type,
    assert_serialization_roundtrip,
    assert_valid_construction,
)

import model as model_module
from model import TradingPlatform

REQUIRED = ["name", "code"]
NON_NULLABLE = ["id", *REQUIRED, "is_active"]


def _valid() -> dict:
    return {"id": 1, "name": "MetaTrader 5", "code": "metatrader_5"}


def test_public_interface():
    assert_public_interface(model_module, "TradingPlatform", TradingPlatform)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(TradingPlatform, _valid())
    assert instance.is_active is True
    assert instance.description is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(TradingPlatform, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(TradingPlatform, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(TradingPlatform, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(TradingPlatform, _valid(), "code")


def test_serialization_roundtrip():
    assert_serialization_roundtrip(TradingPlatform(**_valid()))
