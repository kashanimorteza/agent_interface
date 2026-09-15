"""Verifies the repeatable Initial Data Seed/Import entry point."""

from __future__ import annotations

from model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    TradingPlatform,
    TrailingGroup,
    User,
)

from database.interface import DatabaseInterface
from database.seed import seed_initial_data

EXPECTED_COUNTS: dict[type, int] = {
    User: 1,
    TradingPlatform: 2,
    Instance: 1,
    Currency: 8,
    Broker: 1,
    Asset: 4,
    AccountGroup: 1,
    Account: 1,
    TrailingGroup: 1,
    PartialGroup: 1,
    ActionGroup: 1,
    Action: 1,
}


def test_seed_creates_every_declared_initial_data_record(db: DatabaseInterface) -> None:
    seed_initial_data(db)
    for model_cls, expected in EXPECTED_COUNTS.items():
        assert len(db.list(model_cls)) == expected, model_cls.__name__


def test_seed_relationships_are_satisfied(db: DatabaseInterface) -> None:
    seed_initial_data(db)
    instance = db.list(Instance)[0]
    mt5 = db.search(TradingPlatform, {"name": "MetaTrader 5"})[0]
    assert instance.trading_platform_id == mt5.id

    account = db.list(Account)[0]
    usd = db.search(Currency, {"code": "USD"})[0]
    assert account.base_currency_id == usd.id
    assert account.instance_id == instance.id

    action = db.list(Action)[0]
    eur_usd = db.search(Asset, {"symbol": "EUR/USD"})[0]
    assert action.asset_id == eur_usd.id
    assert action.account_id == account.id


def test_seed_is_idempotent(db: DatabaseInterface) -> None:
    first_admin = seed_initial_data(db)
    second_admin = seed_initial_data(db)
    assert first_admin.id == second_admin.id
    for model_cls, expected in EXPECTED_COUNTS.items():
        assert len(db.list(model_cls)) == expected, model_cls.__name__


def test_seed_generates_credentials_that_are_not_plaintext(
    db: DatabaseInterface,
) -> None:
    admin = seed_initial_data(db)
    assert admin.password != "Admin"
    assert len(admin.password) > 0
