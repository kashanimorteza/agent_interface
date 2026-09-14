"""Verification for the Instance Domain Definition (Task P1-instance)."""

from __future__ import annotations

from conftest import (
    assert_public_interface,
    assert_rejects_missing_required,
    assert_rejects_null_for_non_nullable,
    assert_rejects_unknown_field,
    assert_rejects_wrong_type,
    assert_serialization_roundtrip,
    assert_valid_construction,
)

import model as model_module
from model import Instance

REQUIRED = ["user_id", "name", "trading_platform_id"]
NON_NULLABLE = ["id", *REQUIRED, "is_active"]


def _valid() -> dict:
    return {
        "id": 1,
        "user_id": 1,
        "name": "MetaTrader",
        "trading_platform_id": 1,
        "ip": "127.0.0.1",
        "username": "test",
        "password": "s3cret",
        "api_key": "key-123",
    }


def test_public_interface():
    assert_public_interface(model_module, "Instance", Instance)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(Instance, _valid())
    assert instance.is_active is True
    assert instance.description is None


def test_optional_connection_fields_default_to_none():
    data = {"id": 1, "user_id": 1, "name": "MetaTrader", "trading_platform_id": 1}
    instance = Instance(**data)
    assert instance.ip is None
    assert instance.username is None
    assert instance.password is None
    assert instance.api_key is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Instance, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(Instance, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(Instance, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(Instance, _valid(), "user_id")


def test_reports_declared_credential_storage():
    assert Instance.credential_storage() == {
        "password": "encrypted",
        "api_key": "encrypted",
    }


def test_serialization_roundtrip():
    assert_serialization_roundtrip(Instance(**_valid()))
