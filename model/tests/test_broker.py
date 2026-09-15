from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import Broker

VALID = {"name": "FxPro", "user_id": 1}


def test_valid_construction_applies_declared_defaults():
    broker = Broker.model_validate(VALID)
    assert broker.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Broker, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("name", "user_id"):
        assert_requires_field(Broker, VALID, field)


def test_publishes_relationship_and_uniqueness_metadata():
    contract = Broker.persistence_contract()
    assert ("user_id", "name") in contract.unique_sets
    assert contract.relationships[0].references == "User"


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(Broker.model_validate(VALID))
