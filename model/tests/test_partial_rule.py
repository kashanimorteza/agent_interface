"""Verification for the Partial Rule Domain Definition (Task P1-partial-rule)."""

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
from model import PartialRule

REQUIRED = ["name", "partial_group_id", "profit_percentage", "close_percentage"]
NON_NULLABLE = ["id", *REQUIRED, "is_active"]


def _valid() -> dict:
    return {
        "id": 1,
        "name": "PR-1",
        "partial_group_id": 1,
        "profit_percentage": decimal.Decimal(25),
        "close_percentage": decimal.Decimal(50),
    }


def test_public_interface():
    assert_public_interface(model_module, "PartialRule", PartialRule)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(PartialRule, _valid())
    assert instance.is_active is True


def test_profit_percentage_rejects_float_input():
    data = _valid()
    data["profit_percentage"] = 25.0
    with pytest.raises(pydantic.ValidationError):
        PartialRule(**data)


def test_rejects_unknown_field():
    assert_rejects_unknown_field(PartialRule, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(PartialRule, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(PartialRule, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(PartialRule, _valid(), "partial_group_id")


def test_serialization_roundtrip():
    assert_serialization_roundtrip(PartialRule(**_valid()))
