"""Tests for Asset, Account Group, and Account."""

import pytest
from pydantic import ValidationError

from model.account import Account
from model.account_group import AccountGroup
from model.asset import Asset
from model.foundation import ForeignKey, persistence_contract


def test_asset_defaults_relationship_and_uniqueness() -> None:
    asset = Asset(broker_id=1, symbol="EUR/USD", category="Currency", point_size=0.0001, digits=5)
    assert asset.is_active is True

    contract = persistence_contract(Asset)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["broker_id"].foreign_key == ForeignKey("Broker", "id")
    assert contract.unique_sets == (("broker_id", "symbol"),)

    with pytest.raises(ValidationError):
        Asset(broker_id=1, category="Currency")  # type: ignore[call-arg]


def test_account_group_relationship_and_uniqueness() -> None:
    group = AccountGroup(user_id=1, name="Default")
    assert group.is_active is True

    contract = persistence_contract(AccountGroup)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["user_id"].foreign_key == ForeignKey("User", "id")
    assert contract.unique_sets == (("user_id", "name"),)


def test_account_relationships_credential_and_composite_uniqueness() -> None:
    account = Account(
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
    assert account.balance == 0
    assert account.is_active is True

    contract = persistence_contract(Account)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["group_id"].foreign_key == ForeignKey("AccountGroup", "id")
    assert by_name["broker_id"].foreign_key == ForeignKey("Broker", "id")
    assert by_name["instance_id"].foreign_key == ForeignKey("Instance", "id")
    assert by_name["base_currency_id"].foreign_key == ForeignKey("Currency", "id")
    assert by_name["password"].credential == "encrypted"
    assert by_name["name"].unique is True
    assert contract.unique_sets == (("group_id", "broker_id", "instance_id"),)

    with pytest.raises(ValidationError):
        Account(
            name="Acc-2",
            group_id=1,
            broker_id=1,
            instance_id=1,
            base_currency_id=1,
            username="test",
            password="secret",
            account_type="CFD",
        )  # type: ignore[call-arg]
