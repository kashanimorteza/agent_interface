"""Insert the Target-declared initial data through the Database Interface, in dependency order.

Safe to re-run: skips insertion when the initial User record already exists.
"""

import secrets

from my_database import Database
from my_model import (
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


def _secret(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def seed() -> None:
    existing = Database.list(User, filters={"username": "admin"})
    if existing:
        print("Initial data already present (admin User found); nothing to do.")
        return

    user = Database.add(User(name="Admin", username="admin", password=_secret(), api_key=_secret()))

    mt5 = Database.add(TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    Database.add(TradingPlatform(name="Binance", code="binance"))

    instance = Database.add(
        Instance(
            user_id=user.id,
            trading_platform_id=mt5.id,
            name="MetaTrader",
            ip="127.0.0.1",
            username="test",
            password=_secret(),
            api_key=_secret(),
        )
    )

    currencies = [
        ("USD", "$", "United States", 2),
        ("EUR", "€", "Eurozone", 2),
        ("GBP", "£", "United Kingdom", 2),
        ("JPY", "¥", "Japan", 0),
        ("CHF", "CHF", "Switzerland", 2),
        ("CAD", "C$", "Canada", 2),
        ("AUD", "A$", "Australia", 2),
        ("NZD", "NZ$", "New Zealand", 2),
    ]
    usd = None
    for code, symbol, country, digits in currencies:
        currency = Database.add(
            Currency(user_id=user.id, code=code, symbol=symbol, country=country, decimal_digits=digits)
        )
        if code == "USD":
            usd = currency

    broker = Database.add(Broker(name="FxPro", user_id=user.id))

    assets = [
        ("EUR/USD", "Currency", 0.0001, 5),
        ("EUR/GBP", "Currency", 0.001, 5),
        ("XAU/USD", "Commodity", 0.01, 2),
        ("USOil", "Commodity", 0.01, 3),
    ]
    first_asset = None
    for symbol, category, point_size, digits in assets:
        asset = Database.add(
            Asset(broker_id=broker.id, symbol=symbol, category=category, point_size=point_size, digits=digits)
        )
        if first_asset is None:
            first_asset = asset

    account_group = Database.add(AccountGroup(user_id=user.id, name="Default"))

    account = Database.add(
        Account(
            name="Acc-1",
            group_id=account_group.id,
            broker_id=broker.id,
            instance_id=instance.id,
            base_currency_id=usd.id,
            username="test",
            password=_secret(),
            leverage=100,
            account_type="CFD",
        )
    )

    trailing_group = Database.add(TrailingGroup(user_id=user.id, name="Default"))
    partial_group = Database.add(PartialGroup(user_id=user.id, name="Default"))
    action_group = Database.add(ActionGroup(user_id=user.id, name="Default"))

    Database.add(
        Action(
            name="Default",
            action_group_id=action_group.id,
            asset_id=first_asset.id,
            account_id=account.id,
            partial_group_id=partial_group.id,
            trailing_group_id=trailing_group.id,
            risk_by_reward=1,
            take_profit=1,
            stop_loss=1,
        )
    )

    print("Initial data inserted.")


if __name__ == "__main__":
    seed()
