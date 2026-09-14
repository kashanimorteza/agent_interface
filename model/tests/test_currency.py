"""Tests for the Currency Domain Definition (task P1-G3-T1)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Currency


def _make() -> Currency:
    return Currency(user_id=1, code="USD")


def test_exact_field_set() -> None:
    assert set(Currency.model_fields) == {
        "id",
        "user_id",
        "code",
        "symbol",
        "country",
        "decimal_digits",
        "is_active",
        "description",
    }


def test_uniqueness_on_user_and_code() -> None:
    assert Currency.UNIQUE_CONSTRAINTS == (("user_id", "code"),)


def test_code_size_enforced_both_directions() -> None:
    with pytest.raises(ValidationError):
        Currency(user_id=1, code="US")
    with pytest.raises(ValidationError):
        Currency(user_id=1, code="USDX")
    Currency(user_id=1, code="USD")


def test_decimal_digits_default() -> None:
    assert _make().decimal_digits == 2


def test_json_round_trip_and_schema() -> None:
    currency = _make()
    restored = Currency.model_validate_json(currency.model_dump_json())
    assert restored == currency
    assert Currency.model_json_schema()["properties"]
