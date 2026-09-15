"""Validation behavior, serialization, and persistence metadata for every Domain Definition."""

from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from model import Credential, DomainModel

ALL_FIXTURES = [
    "user",
    "trading_platform",
    "instance",
    "currency",
    "broker",
    "asset",
    "account_group",
    "account",
    "trailing_group",
    "trailing_rule",
    "partial_group",
    "partial_rule",
    "action_group",
    "action",
    "position",
]


@pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
def test_round_trips_through_dict_without_data_loss(fixture_name: str, request):
    instance: DomainModel = request.getfixturevalue(fixture_name)
    rebuilt = type(instance).model_validate(instance.model_dump())
    assert rebuilt == instance


@pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
def test_round_trips_through_json_without_data_loss(fixture_name: str, request):
    instance: DomainModel = request.getfixturevalue(fixture_name)
    rebuilt = type(instance).model_validate_json(instance.model_dump_json())
    assert rebuilt == instance


@pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
def test_generates_a_json_schema(fixture_name: str, request):
    instance: DomainModel = request.getfixturevalue(fixture_name)
    schema = type(instance).model_json_schema()
    assert schema["title"] == type(instance).__name__
    assert set(instance.model_dump()) <= set(schema["properties"])


@pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
def test_rejects_construction_missing_a_required_field(fixture_name: str, request):
    instance: DomainModel = request.getfixturevalue(fixture_name)
    data = instance.model_dump()
    required_fields = [
        name for name, info in type(instance).model_fields.items() if info.is_required()
    ]
    assert required_fields, "every Domain Definition declares at least one required field"
    del data[required_fields[0]]
    with pytest.raises(ValidationError):
        type(instance).model_validate(data)


@pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
def test_rejects_an_undeclared_field(fixture_name: str, request):
    instance: DomainModel = request.getfixturevalue(fixture_name)
    data = instance.model_dump()
    data["undeclared_field"] = "unexpected"
    with pytest.raises(ValidationError):
        type(instance).model_validate(data)


@pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
def test_persistence_metadata_reports_declared_primary_key(fixture_name: str, request):
    instance: DomainModel = request.getfixturevalue(fixture_name)
    metadata = type(instance).persistence_metadata()
    assert metadata["persistent"] is True
    assert metadata["primary_key"] == ("id",)
    assert metadata["auto_increment"] == ("id",)
    assert metadata["fields"]["id"]["required"] is True
    assert metadata["fields"]["id"]["nullable"] is False


def test_user_credentials_require_hash_treatment(user):
    metadata = type(user).persistence_metadata()
    assert metadata["credentials"]["password"] == Credential.HASH.value
    assert metadata["credentials"]["api_key"] == Credential.HASH.value


def test_instance_credentials_require_encrypted_treatment(instance):
    metadata = type(instance).persistence_metadata()
    assert metadata["credentials"]["password"] == Credential.ENCRYPTED.value
    assert metadata["credentials"]["api_key"] == Credential.ENCRYPTED.value


def test_account_credential_requires_encrypted_treatment(account):
    metadata = type(account).persistence_metadata()
    assert metadata["credentials"]["password"] == Credential.ENCRYPTED.value


def test_account_publishes_its_composite_uniqueness_constraint(account):
    metadata = type(account).persistence_metadata()
    assert ("group_id", "broker_id", "instance_id") in metadata["unique_sets"]


def test_currency_publishes_its_composite_uniqueness_constraint(currency):
    metadata = type(currency).persistence_metadata()
    assert ("user_id", "code") in metadata["unique_sets"]


def test_trailing_rule_publishes_its_composite_uniqueness_constraint(trailing_rule):
    metadata = type(trailing_rule).persistence_metadata()
    assert ("trailing_group_id", "trigger_percentage") in metadata["unique_sets"]


def test_instance_foreign_keys_reference_user_and_trading_platform(instance):
    metadata = type(instance).persistence_metadata()
    assert metadata["foreign_keys"]["user_id"]["target"] == "User"
    assert metadata["foreign_keys"]["user_id"]["cardinality"] == "many_to_one"
    assert metadata["foreign_keys"]["trading_platform_id"]["target"] == "TradingPlatform"


def test_position_foreign_keys_reference_every_declared_relationship(position):
    metadata = type(position).persistence_metadata()
    expected_targets = {
        "user_id": "User",
        "trading_platform_id": "TradingPlatform",
        "broker_id": "Broker",
        "account_id": "Account",
        "trailing_group_id": "TrailingGroup",
        "partial_group_id": "PartialGroup",
        "action_group_id": "ActionGroup",
        "action_id": "Action",
    }
    for field, target in expected_targets.items():
        assert metadata["foreign_keys"][field]["target"] == target


def test_currency_code_respects_its_declared_size(user):
    from model import Currency

    with pytest.raises(ValidationError):
        Currency(id=1, user_id=user.id, code="TOOLONG")


def test_position_date_must_be_timezone_aware(position):
    with pytest.raises(ValidationError):
        type(position).model_validate({**position.model_dump(), "date": datetime(2026, 1, 1)})


def test_decimal_fields_preserve_exact_precision(trailing_rule):
    assert trailing_rule.trigger_percentage == Decimal("50")
    dumped = trailing_rule.model_dump()
    assert dumped["trigger_percentage"] == Decimal("50")


def test_optional_fields_default_to_none(user):
    assert user.description is None


def test_boolean_fields_default_to_declared_value(user, position):
    assert user.is_active is True
    assert position.is_executed is False
