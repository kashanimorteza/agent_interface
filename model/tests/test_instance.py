"""Tests for the Instance Domain Definition (task P1-G2-T3)."""

from __future__ import annotations

from model import Instance


def _make() -> Instance:
    return Instance(user_id=1, name="MetaTrader", trading_platform_id=1)


def test_exact_field_set() -> None:
    assert set(Instance.model_fields) == {
        "id",
        "user_id",
        "name",
        "trading_platform_id",
        "ip",
        "username",
        "password",
        "api_key",
        "is_active",
        "description",
    }


def test_credential_meaning_on_password_and_api_key() -> None:
    assert Instance.model_fields["password"].json_schema_extra == {"credential": True}
    assert Instance.model_fields["api_key"].json_schema_extra == {"credential": True}


def test_uniqueness_on_user_and_name() -> None:
    assert Instance.UNIQUE_CONSTRAINTS == (("user_id", "name"),)


def test_nullable_defaults() -> None:
    instance = _make()
    assert instance.ip is None
    assert instance.username is None
    assert instance.password is None
    assert instance.api_key is None
    assert instance.is_active is True


def test_json_round_trip_and_schema() -> None:
    instance = _make()
    restored = Instance.model_validate_json(instance.model_dump_json())
    assert restored == instance
    assert Instance.model_json_schema()["properties"]
