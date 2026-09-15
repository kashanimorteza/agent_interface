from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import TrailingGroup

VALID = {"user_id": 1, "name": "Default"}


def test_valid_construction_applies_declared_defaults():
    group = TrailingGroup.model_validate(VALID)
    assert group.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(TrailingGroup, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("user_id", "name"):
        assert_requires_field(TrailingGroup, VALID, field)


def test_publishes_relationship_and_uniqueness_metadata():
    contract = TrailingGroup.persistence_contract()
    assert ("user_id", "name") in contract.unique_sets
    assert contract.relationships[0].references == "User"


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(TrailingGroup.model_validate(VALID))
