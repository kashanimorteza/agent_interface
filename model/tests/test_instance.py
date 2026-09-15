from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import Instance

VALID = {
    "user_id": 1,
    "trading_platform_id": 1,
    "name": "MetaTrader",
    "ip": "127.0.0.1",
    "username": "test",
    "password": "encrypted-pw",
    "api_key": "encrypted-key",
}


def test_valid_construction_applies_declared_defaults():
    instance = Instance.model_validate(VALID)
    assert instance.is_active is True
    assert instance.description is None


def test_technical_connection_fields_are_optional():
    minimal = {"user_id": 1, "trading_platform_id": 1, "name": "Bare"}
    instance = Instance.model_validate(minimal)
    assert instance.ip is None
    assert instance.username is None
    assert instance.password is None
    assert instance.api_key is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Instance, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("user_id", "trading_platform_id", "name"):
        assert_requires_field(Instance, VALID, field)


def test_publishes_relationships_and_credential_metadata():
    contract = Instance.persistence_contract()
    assert contract.persistent is True
    assert contract.fields["password"].credential == "encrypted"
    assert contract.fields["api_key"].credential == "encrypted"
    assert ("user_id", "name") in contract.unique_sets
    references = {r.field: r.references for r in contract.relationships}
    assert references == {"user_id": "User", "trading_platform_id": "TradingPlatform"}


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(Instance.model_validate(VALID))
