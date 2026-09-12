from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model.currency import Currency


def test_valid_construction_succeeds() -> None:
    instance = Currency(user_id=1, code="USD")
    assert instance.decimal_digits == 2
    assert instance.status is True


def test_code_must_be_exactly_three_characters() -> None:
    with pytest.raises(ValidationError):
        Currency(user_id=1, code="US")


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Currency(code="USD")  # pyright: ignore[reportCallIssue] - deliberately missing user_id


def test_uniqueness_rule_is_declared() -> None:
    assert Currency.UNIQUE_TOGETHER == (("user_id", "code"),)


def test_declared_initial_records_are_present() -> None:
    assert len(Currency.INITIAL_DATA) == 8
    codes = {record["code"] for record in Currency.INITIAL_DATA}
    assert codes == {"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"}
    for record in Currency.INITIAL_DATA:
        Currency.model_validate(record)
