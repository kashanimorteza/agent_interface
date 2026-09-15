from decimal import Decimal

from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import Account

VALID = {
    "name": "Acc-1",
    "group_id": 1,
    "broker_id": 1,
    "instance_id": 1,
    "base_currency_id": 1,
    "username": "test",
    "password": "encrypted-pw",
    "leverage": 100,
    "account_type": "CFD",
}


def test_valid_construction_applies_declared_defaults():
    account = Account.model_validate(VALID)
    assert account.balance == 0
    assert account.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Account, VALID)


def test_requires_declared_non_nullable_fields():
    for field in (
        "name",
        "group_id",
        "broker_id",
        "instance_id",
        "base_currency_id",
        "username",
        "password",
        "leverage",
        "account_type",
    ):
        assert_requires_field(Account, VALID, field)


def test_publishes_relationships_credential_and_uniqueness_metadata():
    contract = Account.persistence_contract()
    assert contract.fields["password"].credential == "encrypted"
    assert contract.fields["name"].unique is True
    assert ("group_id", "broker_id", "instance_id") in contract.unique_sets
    references = {r.field: r.references for r in contract.relationships}
    assert references == {
        "group_id": "AccountGroup",
        "broker_id": "Broker",
        "instance_id": "Instance",
        "base_currency_id": "Currency",
    }
    assert contract.fields["balance"].default == Decimal(0)


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(Account.model_validate(VALID))
