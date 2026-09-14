"""Verification for the Trailing Rule Domain Definition (Task P1-trailing-rule)."""

from __future__ import annotations

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
from model import TrailingRule

REQUIRED = ["name", "trailing_group_id", "trigger_percentage"]
NON_NULLABLE = ["id", *REQUIRED, "is_active"]


def _valid() -> dict:
    return {
        "id": 1,
        "name": "TR-1",
        "trailing_group_id": 1,
        "trigger_percentage": decimal.Decimal(50),
        "take_profit_adjustment": decimal.Decimal("1.5"),
        "stop_loss_adjustment": decimal.Decimal("0.5"),
    }


def test_public_interface():
    assert_public_interface(model_module, "TrailingRule", TrailingRule)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(TrailingRule, _valid())
    assert instance.is_active is True
    assert instance.description is None


def test_optional_adjustments_default_to_none():
    data = {
        "id": 1,
        "name": "TR-1",
        "trailing_group_id": 1,
        "trigger_percentage": decimal.Decimal(50),
    }
    instance = TrailingRule(**data)
    assert instance.take_profit_adjustment is None
    assert instance.stop_loss_adjustment is None


def test_trigger_percentage_rejects_float_input():
    data = _valid()
    data["trigger_percentage"] = 50.0
    with pytest.raises(pydantic.ValidationError):
        TrailingRule(**data)


def test_rejects_unknown_field():
    assert_rejects_unknown_field(TrailingRule, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(TrailingRule, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(TrailingRule, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(TrailingRule, _valid(), "trailing_group_id")


def test_serialization_roundtrip():
    assert_serialization_roundtrip(TrailingRule(**_valid()))
