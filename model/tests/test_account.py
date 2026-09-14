"""Verifies the Account Domain Definition (Task P1-G4-T2)."""

from __future__ import annotations

from decimal import Decimal

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import Account

EXPECTED_FIELDS = {
    "id": True,
    "name": True,
    "group_id": True,
    "broker_id": True,
    "instance_id": True,
    "base_currency_id": True,
    "username": True,
    "password": True,
    "leverage": True,
    "balance": False,
    "account_type": True,
    "status": False,
    "description": False,
}


def _make(**overrides):
    kwargs = {
        "id": 1,
        "name": "Acc-1",
        "group_id": 1,
        "broker_id": 1,
        "instance_id": 1,
        "base_currency_id": 1,
        "username": "test",
        "password": "secret",
        "leverage": 100,
        "account_type": "CFD",
    }
    kwargs.update(overrides)
    return Account(**kwargs)


def test_matches_target_definition() -> None:
    assert_exact_fields(Account, EXPECTED_FIELDS)
    assert_credential_fields(Account, ("password",))
    assert_unique_constraints(
        Account, (("name",), ("group_id", "broker_id", "instance_id"))
    )


def test_defaults() -> None:
    account = _make()
    assert account.balance == Decimal(0)
    assert account.status is True


def test_balance_keeps_exact_decimal_precision() -> None:
    account = _make(balance=Decimal("1000.55"))
    assert account.balance == Decimal("1000.55")


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        Account(id=1, name="Acc-1")  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    account = _make(balance=Decimal("1000.50"))
    assert Account.model_validate_json(account.model_dump_json()) == account
    assert set(EXPECTED_FIELDS) <= set(Account.model_json_schema()["properties"])
