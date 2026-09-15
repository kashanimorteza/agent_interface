from decimal import Decimal

from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import PartialRule

VALID = {
    "name": "Partial-50",
    "partial_group_id": 1,
    "profit_percentage": Decimal(50),
    "close_percentage": Decimal(25),
}


def test_valid_construction_applies_declared_defaults():
    rule = PartialRule.model_validate(VALID)
    assert rule.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(PartialRule, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("name", "partial_group_id", "profit_percentage", "close_percentage"):
        assert_requires_field(PartialRule, VALID, field)


def test_publishes_relationship_and_uniqueness_metadata():
    contract = PartialRule.persistence_contract()
    assert contract.fields["name"].unique is True
    assert ("partial_group_id", "profit_percentage") in contract.unique_sets
    assert contract.relationships[0].references == "PartialGroup"


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(PartialRule.model_validate(VALID))
