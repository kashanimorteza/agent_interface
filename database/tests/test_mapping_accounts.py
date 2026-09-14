"""Tests for the Accounts storage mappings (tasks P2-G5-T1..T2)."""

from __future__ import annotations

from decimal import Decimal

import model
import pytest

from database.exceptions import ConstraintViolation


def _make_user_broker_instance_currency(db):
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    platform = db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    instance = db.create(
        model.Instance(user_id=user.id, name="MetaTrader", trading_platform_id=platform.id)
    )
    broker = db.create(model.Broker(name="FxPro", user_id=user.id))
    currency = db.create(model.Currency(user_id=user.id, code="USD"))
    return user, broker, instance, currency


def test_account_group_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    created = db.create(model.AccountGroup(user_id=user.id, name="Default"))
    fetched = db.get(model.AccountGroup, created.id)
    assert fetched is not None
    assert fetched.name == "Default"

    with pytest.raises(ConstraintViolation):
        db.create(model.AccountGroup(user_id=user.id, name="Default"))


def test_account_mapping_preserves_fields_relationships_uniqueness_and_credential(db) -> None:
    user, broker, instance, currency = _make_user_broker_instance_currency(db)
    group = db.create(model.AccountGroup(user_id=user.id, name="Default"))

    created = db.create(
        model.Account(
            name="Acc-1",
            group_id=group.id,
            broker_id=broker.id,
            instance_id=instance.id,
            base_currency_id=currency.id,
            username="test",
            password="secret",
            leverage=100,
            account_type="CFD",
        )
    )
    fetched = db.get(model.Account, created.id)
    assert fetched is not None
    assert fetched.group_id == group.id
    assert fetched.broker_id == broker.id
    assert fetched.instance_id == instance.id
    assert fetched.base_currency_id == currency.id
    assert fetched.balance == Decimal("0")
    assert fetched.password != "secret"

    with pytest.raises(ConstraintViolation):
        db.create(
            model.Account(
                name="Acc-1",
                group_id=group.id,
                broker_id=broker.id,
                instance_id=instance.id,
                base_currency_id=currency.id,
                username="test2",
                password="secret2",
                leverage=50,
                account_type="CFD",
            )
        )
