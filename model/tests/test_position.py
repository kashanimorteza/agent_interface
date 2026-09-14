"""Verification for the Position Domain Definition (Task P1-position)."""

from __future__ import annotations

import datetime
import decimal

import pydantic
import pytest
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
from model import Position

REQUIRED = [
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
]
NON_NULLABLE = ["id", *REQUIRED, "is_active", "profit", "is_executed"]


def _valid() -> dict:
    return {
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
        "date": datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        "volume": decimal.Decimal("1.0"),
        "order_type": "market",
        "base_tp": decimal.Decimal("1.1"),
        "base_sl": decimal.Decimal("0.9"),
        "real_tp": decimal.Decimal("1.1"),
        "real_sl": decimal.Decimal("0.9"),
    }


def test_public_interface():
    assert_public_interface(model_module, "Position", Position)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(Position, _valid())
    assert instance.is_active is True
    assert instance.profit == decimal.Decimal(0)
    assert isinstance(instance.profit, decimal.Decimal)
    assert instance.is_executed is False
    assert instance.description is None


def test_date_rejects_naive_datetime():
    data = _valid()
    data["date"] = datetime.datetime(2026, 1, 1)  # noqa: DTZ001 (naive on purpose: proves rejection)
    with pytest.raises(pydantic.ValidationError):
        Position(**data)


def test_volume_rejects_float_input():
    data = _valid()
    data["volume"] = 1.0
    with pytest.raises(pydantic.ValidationError):
        Position(**data)


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Position, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(Position, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(Position, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(Position, _valid(), "account_id")


def test_serialization_roundtrip():
    assert_serialization_roundtrip(Position(**_valid()))
