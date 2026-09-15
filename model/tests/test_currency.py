import pytest
from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)
from pydantic import ValidationError

from model import Currency

VALID = {"user_id": 1, "code": "USD", "symbol": "$", "country": "United States"}


def test_valid_construction_applies_declared_defaults():
    currency = Currency.model_validate(VALID)
    assert currency.decimal_digits == 2
    assert currency.is_active is True


def test_code_must_be_exactly_three_characters():
    with pytest.raises(ValidationError):
        Currency.model_validate({**VALID, "code": "US"})


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Currency, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("user_id", "code"):
        assert_requires_field(Currency, VALID, field)


def test_publishes_relationship_and_uniqueness_metadata():
    contract = Currency.persistence_contract()
    assert ("user_id", "code") in contract.unique_sets
    assert contract.relationships[0].references == "User"
    assert contract.fields["decimal_digits"].default == 2


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(Currency.model_validate(VALID))
