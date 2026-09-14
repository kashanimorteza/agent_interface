"""Verification for the Account Domain Definition (Task P1-account)."""

from __future__ import annotations

import decimal

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
from model import Account

REQUIRED = [
    "name",
    "group_id",
    "broker_id",
    "instance_id",
    "base_currency_id",
    "username",
    "password",
    "leverage",
    "account_type",
]
NON_NULLABLE = ["id", *REQUIRED, "is_active", "balance"]


def _valid() -> dict:
    return {
        "id": 1,
        "name": "Acc-1",
        "group_id": 1,
        "broker_id": 1,
        "instance_id": 1,
        "base_currency_id": 1,
        "username": "test",
        "password": "s3cret",
        "leverage": 100,
        "account_type": "CFD",
    }


def test_public_interface():
    assert_public_interface(model_module, "Account", Account)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(Account, _valid())
    assert instance.is_active is True
    assert instance.balance == decimal.Decimal(0)
    assert isinstance(instance.balance, decimal.Decimal)
    assert instance.description is None


def test_balance_rejects_float_input():
    data = _valid()
    data["balance"] = 12.5
    import pydantic
    import pytest

    with pytest.raises(pydantic.ValidationError):
        Account(**data)


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Account, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(Account, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(Account, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(Account, _valid(), "leverage")


def test_reports_declared_credential_storage():
    assert Account.credential_storage() == {"password": "encrypted"}


def test_serialization_roundtrip():
    assert_serialization_roundtrip(Account(**_valid()))
