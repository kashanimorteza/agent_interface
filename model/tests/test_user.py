"""Tests for the User Domain Definition (task P1-G2-T1)."""

from __future__ import annotations

from model import User


def _make() -> User:
    return User(name="Ada", username="ada", password="secret", api_key="key123")


def test_exact_field_set() -> None:
    assert set(User.model_fields) == {
        "id",
        "name",
        "username",
        "password",
        "api_key",
        "is_active",
        "description",
    }


def test_credential_meaning_on_password_and_api_key() -> None:
    assert User.model_fields["password"].json_schema_extra == {"credential": True}
    assert User.model_fields["api_key"].json_schema_extra == {"credential": True}
    assert User.model_fields["username"].json_schema_extra is None


def test_uniqueness_on_name() -> None:
    assert User.UNIQUE_CONSTRAINTS == (("name",),)


def test_defaults() -> None:
    user = _make()
    assert user.is_active is True
    assert user.description is None
    assert user.id is None


def test_json_round_trip_and_schema() -> None:
    user = _make()
    restored = User.model_validate_json(user.model_dump_json())
    assert restored == user
    schema = User.model_json_schema()
    assert schema["properties"].keys() >= {"name", "username", "password", "api_key"}
