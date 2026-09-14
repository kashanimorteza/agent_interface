"""Verification for the Asset Domain Definition (Task P1-asset)."""

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
from model import Asset

REQUIRED = ["broker_id", "symbol", "category"]
NON_NULLABLE = ["id", *REQUIRED, "is_active", "point_size", "digits"]


def _valid() -> dict:
    return {"id": 1, "broker_id": 1, "symbol": "EUR/USD", "category": "Currency"}


def test_public_interface():
    assert_public_interface(model_module, "Asset", Asset)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(Asset, _valid())
    assert instance.is_active is True
    assert instance.point_size == 0.0
    assert instance.digits == 0
    assert instance.description is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Asset, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(Asset, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(Asset, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(Asset, _valid(), "broker_id")


def test_serialization_roundtrip():
    assert_serialization_roundtrip(Asset(**_valid()))
