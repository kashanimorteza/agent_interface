from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from my_model._initial_data import GENERATE_SECURELY
from my_model.account import Account


def _valid() -> dict[str, object]:
    return {
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


def test_valid_construction_succeeds() -> None:
    instance = Account.model_validate(_valid())
    assert instance.balance == Decimal(0)
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    data = _valid()
    del data["leverage"]
    with pytest.raises(ValidationError):
        Account.model_validate(data)


def test_credential_field_is_declared_sensitive_and_encrypted() -> None:
    schema = Account.model_json_schema()
    assert schema["properties"]["password"].get("credential") is True
    assert schema["properties"]["password"].get("storage_at_rest") == "encrypted"


def test_uniqueness_rules_are_declared() -> None:
    assert Account.UNIQUE_TOGETHER == (
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    )


def test_declared_initial_record_is_present() -> None:
    record = Account.INITIAL_DATA[0]
    assert record["name"] == "Acc-1"
    assert record["password"] is GENERATE_SECURELY
