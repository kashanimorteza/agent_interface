"""Verifies P1T9: the Account Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Account

VALID = {
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


@pytest.mark.parametrize(
    "omit",
    [
        "name",
        "group_id",
        "broker_id",
        "instance_id",
        "base_currency_id",
        "username",
        "password",
        "leverage",
        "account_type",
    ],
)
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        Account(**payload)


def test_valid_account_round_trips_preserving_relationships_and_defaults() -> None:
    account = Account(**VALID)
    restored = Account(**account.model_dump())
    assert restored == account
    assert restored.balance == 0


def test_published_metadata_declares_unique_constraints_and_encrypted_credential() -> (
    None
):
    meta = Account.persistence_metadata()
    assert meta["fields"]["name"]["unique"] is True
    assert meta["unique_sets"] == [["group_id", "broker_id", "instance_id"]]
    assert meta["fields"]["password"]["credential"] == "encrypted"
    assert meta["fields"]["instance_id"]["foreign_key"] == "instance.id"
