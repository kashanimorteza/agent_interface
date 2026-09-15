"""Verifies P2T5-P2T8: the generic Database Interface, activation, Transaction, and controlled command."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest
from model import (
    Account,
    AccountGroup,
    Broker,
    Currency,
    Instance,
    TradingPlatform,
    User,
)
from sqlalchemy.exc import IntegrityError

from database import interface as db


def _make_account(**overrides: object) -> Account:
    tp = db.create(TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    user = db.create(
        User(name="Trader", username="trader", password="pw", api_key="ak")
    )
    assert tp.id is not None
    assert user.id is not None
    instance = db.create(
        Instance(user_id=user.id, trading_platform_id=tp.id, name="MT")
    )
    broker = db.create(Broker(name="FxPro", user_id=user.id))
    currency = db.create(Currency(user_id=user.id, code="USD"))
    group = db.create(AccountGroup(user_id=user.id, name="Default"))
    assert instance.id is not None
    assert broker.id is not None
    assert currency.id is not None
    assert group.id is not None
    values: dict[str, Any] = {
        "name": "Acc-1",
        "group_id": group.id,
        "broker_id": broker.id,
        "instance_id": instance.id,
        "base_currency_id": currency.id,
        "username": "t",
        "password": "pw",
        "leverage": 100,
        "account_type": "CFD",
    }
    values.update(overrides)
    return db.create(Account(**values))


def test_create_get_list_search_update_delete_round_trip(fresh_db: None) -> None:
    account = _make_account()
    assert account.id is not None
    fetched = db.get_by_id(Account, account.id)
    assert fetched.name == "Acc-1"

    listed = db.list_(Account)
    assert len(listed) == 1

    found = db.search(Account, name="Acc-1")
    assert len(found) == 1 and found[0].id == account.id

    updated = db.update(Account(**{**fetched.model_dump(), "leverage": 200}))
    assert updated.leverage == 200
    assert updated.password == fetched.password  # credential untouched by update

    db.delete(Account, account.id)
    assert db.list_(Account) == []


def test_declared_uniqueness_is_enforced_by_database(fresh_db: None) -> None:
    _make_account()
    with pytest.raises(IntegrityError):
        _make_account(
            name="Different-Name"
        )  # same group/broker/instance -> composite unique violation


def test_referenced_record_existence_is_enforced(fresh_db: None) -> None:
    with pytest.raises(IntegrityError):
        db.create(Instance(user_id=999, trading_platform_id=999, name="orphan"))


def test_activation_toggles_only_is_active(fresh_db: None) -> None:
    account = _make_account()
    assert account.id is not None
    disabled = db.set_active(Account, account.id, active=False)
    assert disabled.is_active is False
    assert disabled.name == account.name
    enabled = db.set_active(Account, account.id, active=True)
    assert enabled.is_active is True


def test_activation_rejected_for_model_without_is_active(fresh_db: None) -> None:
    # Every Target-declared Model happens to declare is_active, so this uses a
    # synthetic Domain Definition that does not, to exercise the rejection path.
    from model.foundation import DomainModel

    class _NoActivation(DomainModel):
        __persistent__ = True
        id: int | None = None

    with pytest.raises(db.UnsupportedOperationError):
        db.set_active(_NoActivation, 1, active=False)


def test_transaction_rolls_back_every_operation_on_failure(fresh_db: None) -> None:
    with pytest.raises(IntegrityError), db.transaction() as session:
        session.create(TradingPlatform(name="Temp", code="temp"))
        session.create(TradingPlatform(name="Other", code="other"))
        session.create(
            TradingPlatform(name="Temp", code="temp-again")
        )  # duplicate name -> fails

    # every operation in the failed Transaction is rolled back, including the two that succeeded
    assert db.list_(TradingPlatform) == []


def test_successful_transaction_commits_every_grouped_operation(fresh_db: None) -> None:
    with db.transaction() as session:
        session.create(TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
        session.create(TradingPlatform(name="Binance", code="binance"))
    assert len(db.list_(TradingPlatform)) == 2


def test_controlled_command_participates_in_transaction_and_is_allow_listed(
    fresh_db: None,
) -> None:
    account = _make_account()
    result = db.execute_command(
        "increment_account_balance", account_id=account.id, delta=Decimal(25)
    )
    assert result.balance == Decimal(25)


def test_unlisted_controlled_command_is_rejected(fresh_db: None) -> None:
    with pytest.raises(db.UnsupportedOperationError):
        db.execute_command("drop_table", table="accounts")
