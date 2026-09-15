from decimal import Decimal

from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import TrailingRule

VALID = {"name": "Trail-50", "trailing_group_id": 1, "trigger_percentage": Decimal(50)}


def test_valid_construction_applies_declared_defaults():
    rule = TrailingRule.model_validate(VALID)
    assert rule.is_active is True
    assert rule.take_profit_adjustment is None
    assert rule.stop_loss_adjustment is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(TrailingRule, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("name", "trailing_group_id", "trigger_percentage"):
        assert_requires_field(TrailingRule, VALID, field)


def test_publishes_relationship_and_uniqueness_metadata():
    contract = TrailingRule.persistence_contract()
    assert contract.fields["name"].unique is True
    assert ("trailing_group_id", "trigger_percentage") in contract.unique_sets
    assert contract.relationships[0].references == "TrailingGroup"


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(TrailingRule.model_validate(VALID))
