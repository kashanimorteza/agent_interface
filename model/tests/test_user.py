"""Verification for the User Domain Definition (Task P1-user)."""

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
from model import User

REQUIRED = ["name", "username", "password", "api_key"]
NON_NULLABLE = ["id", *REQUIRED, "is_active"]


def _valid() -> dict:
    return {
        "id": 1,
        "name": "Admin",
        "username": "admin",
        "password": "s3cret",
        "api_key": "key-123",
    }


def test_public_interface():
    assert_public_interface(model_module, "User", User)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(User, _valid())
    assert instance.is_active is True
    assert instance.description is None


def test_rejects_unknown_field():
    assert_rejects_unknown_field(User, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(User, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(User, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(User, _valid(), "name")


def test_reports_declared_credential_storage():
    assert User.credential_storage() == {"password": "hash", "api_key": "hash"}


def test_serialization_roundtrip():
    assert_serialization_roundtrip(User(**_valid()))
