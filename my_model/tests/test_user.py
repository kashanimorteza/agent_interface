"""User model: construction, validation, credential meaning, initial data."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model._initial_data import GENERATE_SECURELY
from my_model.user import User


def _valid() -> dict[str, object]:
    return {"name": "Ada", "username": "ada", "password": "secret", "api_key": "key"}


def test_valid_construction_succeeds() -> None:
    instance = User.model_validate(_valid())
    assert instance.name == "Ada"
    assert instance.status is True
    assert instance.id is None


def test_missing_required_field_is_rejected() -> None:
    data = _valid()
    del data["username"]
    with pytest.raises(ValidationError):
        User.model_validate(data)


def test_unknown_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        User.model_validate({**_valid(), "unexpected": "value"})


def test_credential_fields_are_declared_sensitive() -> None:
    schema = User.model_json_schema()
    for field in ("password", "api_key"):
        assert schema["properties"][field].get("credential") is True


def test_credential_fields_are_excluded_from_repr() -> None:
    instance = User.model_validate(_valid())
    assert "secret" not in repr(instance)
    assert "key" not in repr(instance)


def test_uniqueness_rule_is_declared() -> None:
    assert User.UNIQUE_TOGETHER == (("name",),)


def test_declared_initial_record_is_present() -> None:
    assert len(User.INITIAL_DATA) == 1
    record = User.INITIAL_DATA[0]
    assert record["name"] == "Admin"
    assert record["username"] == "admin"
    assert record["password"] is GENERATE_SECURELY
    assert record["api_key"] is GENERATE_SECURELY


def test_serialization_round_trip() -> None:
    instance = User.model_validate(_valid())
    dumped = instance.model_dump()
    assert dumped["name"] == "Ada"
    assert User.model_validate(dumped) == instance
