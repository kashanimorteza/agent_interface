from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import TradingPlatform

VALID = {"name": "MetaTrader 5", "code": "metatrader_5"}


def test_valid_construction_applies_declared_defaults():
    platform = TradingPlatform.model_validate(VALID)
    assert platform.is_active is True
    assert platform.description is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(TradingPlatform, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("name", "code"):
        assert_requires_field(TradingPlatform, VALID, field)


def test_publishes_uniqueness_metadata():
    contract = TradingPlatform.persistence_contract()
    assert contract.persistent is True
    assert contract.fields["name"].unique is True


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(TradingPlatform.model_validate(VALID))
