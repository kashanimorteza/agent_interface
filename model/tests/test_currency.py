"""Verifies the Currency Domain Definition (Task P1-G3-T1)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import Currency

EXPECTED_FIELDS = {
    "id": True,
    "user_id": True,
    "code": True,
    "symbol": False,
    "country": False,
    "decimal_digits": False,
    "status": False,
    "description": False,
}


def test_matches_target_definition() -> None:
    assert_exact_fields(Currency, EXPECTED_FIELDS)
    assert_credential_fields(Currency, ())
    assert_unique_constraints(Currency, (("user_id", "code"),))


def test_defaults() -> None:
    currency = Currency(id=1, user_id=1, code="USD")
    assert currency.decimal_digits == 2
    assert currency.status is True
    assert currency.symbol is None


def test_code_size_enforced() -> None:
    with pytest.raises(ValidationError):
        Currency(id=1, user_id=1, code="US")
    with pytest.raises(ValidationError):
        Currency(id=1, user_id=1, code="USDX")


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        Currency(id=1, user_id=1)  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    currency = Currency(id=1, user_id=1, code="EUR", symbol="E", country="Eurozone")
    assert Currency.model_validate_json(currency.model_dump_json()) == currency
    assert set(EXPECTED_FIELDS) <= set(Currency.model_json_schema()["properties"])
