from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import Asset

VALID = {"broker_id": 1, "symbol": "EUR/USD", "category": "Currency"}


def test_valid_construction_applies_declared_defaults():
    asset = Asset.model_validate(VALID)
    assert asset.point_size == 0.0
    assert asset.digits == 0
    assert asset.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Asset, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("broker_id", "symbol", "category"):
        assert_requires_field(Asset, VALID, field)


def test_publishes_relationship_and_uniqueness_metadata():
    contract = Asset.persistence_contract()
    assert ("broker_id", "symbol") in contract.unique_sets
    assert contract.relationships[0].references == "Broker"
    assert contract.fields["point_size"].default == 0.0
    assert contract.fields["digits"].default == 0


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(Asset.model_validate(VALID))
