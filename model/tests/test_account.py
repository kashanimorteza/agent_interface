"""Tests for the Account Domain Definition (task P1-G4-T2)."""

from __future__ import annotations

from decimal import Decimal

from model import Account


def _make() -> Account:
    return Account(
        name="Acc-1",
        group_id=1,
        broker_id=1,
        instance_id=1,
        base_currency_id=1,
        username="test",
        password="secret",
        leverage=100,
        account_type="CFD",
    )


def test_exact_field_set() -> None:
    assert set(Account.model_fields) == {
        "id",
        "name",
        "group_id",
        "broker_id",
        "instance_id",
        "base_currency_id",
        "username",
        "password",
        "leverage",
        "balance",
        "account_type",
        "is_active",
        "description",
    }


def test_credential_meaning_on_password() -> None:
    assert Account.model_fields["password"].json_schema_extra == {"credential": True}


def test_both_uniqueness_groups() -> None:
    assert Account.UNIQUE_CONSTRAINTS == (
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    )


def test_exact_decimal_balance_precision() -> None:
    account = _make()
    assert account.balance == Decimal("0")
    priced = account.model_copy(update={"balance": Decimal("1234.5678")})
    assert priced.balance == Decimal("1234.5678")


def test_json_round_trip_and_schema() -> None:
    account = _make()
    restored = Account.model_validate_json(account.model_dump_json())
    assert restored == account
    assert Account.model_json_schema()["properties"]
