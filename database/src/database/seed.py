import secrets
from decimal import Decimal
from typing import Protocol

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
from pydantic import SecretStr

from . import interface as db


class _HasId(Protocol):
    id: int | None


def _generate_secret() -> str:
    return secrets.token_urlsafe(24)


def _id(row: _HasId) -> int:
    assert row.id is not None
    return row.id


def seed_initial_data(*, instance: str | None = None) -> dict[str, str]:
    generated: dict[str, str] = {}

    with db.transaction(instance) as tx:
        existing_users = db.list_(User, session=tx, name="Admin")
        if existing_users:
            admin = existing_users[0]
        else:
            password = _generate_secret()
            api_key = _generate_secret()
            admin = db.create(
                User(
                    name="Admin",
                    username="admin",
                    password=SecretStr(password),
                    api_key=SecretStr(api_key),
                ),
                session=tx,
            )
            generated["User.Admin.password"] = password
            generated["User.Admin.api_key"] = api_key

        platforms: dict[str, TradingPlatform] = {}
        for name, code in (("MetaTrader 5", "metatrader_5"), ("Binance", "binance")):
            existing = db.list_(TradingPlatform, session=tx, code=code)
            platforms[code] = (
                existing[0]
                if existing
                else db.create(TradingPlatform(name=name, code=code), session=tx)
            )

        currencies: dict[str, Currency] = {}
        for code, symbol, country, digits in (
            ("USD", "$", "United States", 2),
            ("EUR", "€", "Eurozone", 2),
            ("GBP", "£", "United Kingdom", 2),
            ("JPY", "¥", "Japan", 0),
            ("CHF", "CHF", "Switzerland", 2),
            ("CAD", "C$", "Canada", 2),
            ("AUD", "A$", "Australia", 2),
            ("NZD", "NZ$", "New Zealand", 2),
        ):
            existing = db.list_(Currency, session=tx, user_id=_id(admin), code=code)
            currencies[code] = (
                existing[0]
                if existing
                else db.create(
                    Currency(
                        user_id=_id(admin),
                        code=code,
                        symbol=symbol,
                        country=country,
                        decimal_digits=digits,
                    ),
                    session=tx,
                )
            )

        existing_brokers = db.list_(
            Broker, session=tx, user_id=_id(admin), name="FxPro"
        )
        broker = (
            existing_brokers[0]
            if existing_brokers
            else db.create(Broker(name="FxPro", user_id=_id(admin)), session=tx)
        )

        existing_instances = db.list_(
            Instance, session=tx, user_id=_id(admin), name="MetaTrader"
        )
        if existing_instances:
            instance_row = existing_instances[0]
        else:
            instance_password = _generate_secret()
            instance_api_key = _generate_secret()
            instance_row = db.create(
                Instance(
                    user_id=_id(admin),
                    name="MetaTrader",
                    trading_platform_id=_id(platforms["metatrader_5"]),
                    ip="127.0.0.1",
                    username="test",
                    password=SecretStr(instance_password),
                    api_key=SecretStr(instance_api_key),
                ),
                session=tx,
            )
            generated["Instance.MetaTrader.password"] = instance_password
            generated["Instance.MetaTrader.api_key"] = instance_api_key

        assets: dict[str, Asset] = {}
        for symbol, category, point_size, digits in (
            ("EUR/USD", "Currency", 0.0001, 5),
            ("EUR/GBP", "Currency", 0.001, 5),
            ("XAU/USD", "Commodity", 0.01, 2),
            ("USOil", "Commodity", 0.01, 3),
        ):
            existing = db.list_(Asset, session=tx, broker_id=_id(broker), symbol=symbol)
            assets[symbol] = (
                existing[0]
                if existing
                else db.create(
                    Asset(
                        broker_id=_id(broker),
                        symbol=symbol,
                        category=category,
                        point_size=point_size,
                        digits=digits,
                    ),
                    session=tx,
                )
            )

        existing_account_groups = db.list_(
            AccountGroup, session=tx, user_id=_id(admin), name="Default"
        )
        account_group = (
            existing_account_groups[0]
            if existing_account_groups
            else db.create(AccountGroup(user_id=_id(admin), name="Default"), session=tx)
        )

        existing_trailing_groups = db.list_(
            TrailingGroup, session=tx, user_id=_id(admin), name="Default"
        )
        trailing_group = (
            existing_trailing_groups[0]
            if existing_trailing_groups
            else db.create(
                TrailingGroup(user_id=_id(admin), name="Default"), session=tx
            )
        )

        existing_partial_groups = db.list_(
            PartialGroup, session=tx, user_id=_id(admin), name="Default"
        )
        partial_group = (
            existing_partial_groups[0]
            if existing_partial_groups
            else db.create(PartialGroup(user_id=_id(admin), name="Default"), session=tx)
        )

        existing_action_groups = db.list_(
            ActionGroup, session=tx, user_id=_id(admin), name="Default"
        )
        action_group = (
            existing_action_groups[0]
            if existing_action_groups
            else db.create(ActionGroup(user_id=_id(admin), name="Default"), session=tx)
        )

        existing_accounts = db.list_(Account, session=tx, name="Acc-1")
        if existing_accounts:
            account = existing_accounts[0]
        else:
            account_password = _generate_secret()
            account = db.create(
                Account(
                    name="Acc-1",
                    group_id=_id(account_group),
                    broker_id=_id(broker),
                    instance_id=_id(instance_row),
                    base_currency_id=_id(currencies["USD"]),
                    username="test",
                    password=SecretStr(account_password),
                    leverage=100,
                    account_type="CFD",
                ),
                session=tx,
            )
            generated["Account.Acc-1.password"] = account_password

        existing_actions = db.list_(
            Action, session=tx, action_group_id=_id(action_group), name="Default"
        )
        if not existing_actions:
            db.create(
                Action(
                    name="Default",
                    action_group_id=_id(action_group),
                    asset_id=_id(assets["EUR/USD"]),
                    account_id=_id(account),
                    partial_group_id=_id(partial_group),
                    trailing_group_id=_id(trailing_group),
                    risk_by_reward=Decimal(1),
                    take_profit=Decimal(1),
                    stop_loss=Decimal(1),
                ),
                session=tx,
            )

    return generated
