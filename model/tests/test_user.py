from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import User

VALID = {
    "name": "Ada Trader",
    "username": "ada",
    "password": "hashed-pw",
    "api_key": "hashed-key",
}


def test_valid_construction_applies_declared_defaults():
    user = User.model_validate(VALID)
    assert user.is_active is True
    assert user.description is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(User, VALID)


def test_requires_declared_non_nullable_fields():
    for field in ("name", "username", "password", "api_key"):
        assert_requires_field(User, VALID, field)


def test_publishes_credential_and_uniqueness_metadata():
    contract = User.persistence_contract()
    assert contract.persistent is True
    assert contract.fields["password"].credential == "hash"
    assert contract.fields["api_key"].credential == "hash"
    assert contract.fields["name"].unique is True
    assert contract.fields["username"].unique is True
    assert contract.fields["is_active"].default is True


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(User.model_validate(VALID))
