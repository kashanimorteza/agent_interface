"""Verification for the Currency Domain Definition (Task P1-currency)."""

from __future__ import annotations

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
from model import Currency

REQUIRED = ["user_id", "code"]
NON_NULLABLE = ["id", *REQUIRED, "is_active", "decimal_digits"]


def _valid() -> dict:
    return {
        "id": 1,
        "user_id": 1,
        "code": "USD",
        "symbol": "$",
        "country": "United States",
    }


def test_public_interface():
    assert_public_interface(model_module, "Currency", Currency)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(Currency, _valid())
    assert instance.is_active is True
    assert instance.decimal_digits == 2
    assert instance.description is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Currency, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(Currency, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(Currency, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(Currency, _valid(), "user_id")


@pytest.mark.parametrize("code", ["US", "USDX", ""])
def test_code_must_be_exactly_three_characters(code: str):
    data = _valid()
    data["code"] = code
    with pytest.raises(pydantic.ValidationError):
        Currency(**data)


def test_serialization_roundtrip():
    assert_serialization_roundtrip(Currency(**_valid()))
