"""Serialization and schema check."""

import json

import my_model


def test_model_dump_round_trips_through_construction() -> None:
    original = my_model.User(id=1, name="Admin", username="admin", password="x", api_key="y")
    dumped = original.model_dump()
    reconstructed = my_model.User(**dumped)
    assert reconstructed == original


def test_model_dump_json_produces_valid_json() -> None:
    currency = my_model.Currency(id=1, user_id=1, code="USD", symbol="$")
    payload = currency.model_dump_json()
    assert json.loads(payload)["code"] == "USD"


def test_model_json_schema_is_generated_and_marks_credential_fields() -> None:
    schema = my_model.User.model_json_schema()
    assert schema["title"] == "User"
    assert schema["properties"]["password"]["credential"] is True
    assert schema["properties"]["password"]["storage_at_rest"] == "hash"


def test_serialization_is_deterministic() -> None:
    account_group = my_model.AccountGroup(id=1, user_id=1, name="Default")
    assert account_group.model_dump() == account_group.model_dump()
    assert account_group.model_dump_json() == account_group.model_dump_json()
