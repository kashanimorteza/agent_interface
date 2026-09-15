"""Verifies P1T5: the Currency Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Currency

VALID = {"id": 1, "user_id": 1, "code": "USD"}


@pytest.mark.parametrize("omit", ["user_id", "code"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        Currency(**payload)


def test_valid_currency_uses_declared_default_decimal_digits() -> None:
    currency = Currency(**VALID)
    assert currency.decimal_digits == 2
    restored = Currency(**currency.model_dump())
    assert restored == currency


def test_published_metadata_declares_composite_unique() -> None:
    meta = Currency.persistence_metadata()
    assert meta["unique_sets"] == [["user_id", "code"]]
