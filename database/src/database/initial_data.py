"""Insert the Target's defined Initial Data into an Instance through Database's own Operations.

Run `python -m database.initial_data` to populate the default Instance once, after it is provisioned.

Records are inserted in the order the Target lists them, so that each record receives the identity that the
Target's Reference values assume. Credentials the Initial Data leaves to be generated are generated securely,
protected as the Target declares (User credentials hashed, Instance and Account credentials encrypted), and
handed to the Human through the secrets directory. They are never printed or logged.
"""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from model.interface import (
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

from database import credentials, data
from database import interface as db


@dataclass
class Context:
    """State shared by the insert steps.

    Attributes:
        instance (str | None): Key of the Instance to populate, or None for the default Instance.
        key (bytes): Encryption key for Instance and Account credentials.
        plain (dict[str, dict[str, str]]): Generated plaintext credentials by record.
    """

    instance: str | None
    key: bytes
    plain: dict[str, dict[str, str]]


def insert_user(context: Context) -> None:
    """Insert the defined User with hashed generated credentials."""
    plain = context.plain["user"]
    db.add(
        User(
            name="Admin",
            username="admin",
            password=credentials.hash_secret(plain["password"]),
            api_key=credentials.hash_secret(plain["api_key"]),
        ),
        context.instance,
    )


def insert_trading_platforms(context: Context) -> None:
    """Insert the defined Trading Platforms."""
    db.add(TradingPlatform(name="MetaTrader 5", code="metatrader_5"), context.instance)
    db.add(TradingPlatform(name="Binance", code="binance"), context.instance)


def insert_instance(context: Context) -> None:
    """Insert the defined Instance with encrypted generated credentials."""
    plain = context.plain["instance"]
    db.add(
        Instance(
            name=plain["name"],
            user_id=1,
            trading_platform_id=1,
            ip="127.0.0.1",
            username="test",
            password=credentials.encrypt(plain["password"], context.key),
            api_key=credentials.encrypt(plain["api_key"], context.key),
        ),
        context.instance,
    )


def insert_currencies(context: Context) -> None:
    """Insert the defined Currencies."""
    for code, symbol, country, decimal_digits in (
        ("USD", "$", "United States", 2),
        ("EUR", "€", "Eurozone", 2),
        ("GBP", "£", "United Kingdom", 2),
        ("JPY", "¥", "Japan", 0),
        ("CHF", "CHF", "Switzerland", 2),
        ("CAD", "C$", "Canada", 2),
        ("AUD", "A$", "Australia", 2),
        ("NZD", "NZ$", "New Zealand", 2),
    ):
        currency = Currency(
            user_id=1,
            code=code,
            symbol=symbol,
            country=country,
            decimal_digits=decimal_digits,
        )
        db.add(currency, context.instance)


def insert_broker(context: Context) -> None:
    """Insert the defined Broker."""
    db.add(Broker(name="FxPro", user_id=1), context.instance)


def insert_assets(context: Context) -> None:
    """Insert the defined Assets."""
    for symbol, category, point_size, digits in (
        ("EUR/USD", "Currency", 0.0001, 5),
        ("EUR/GBP", "Currency", 0.001, 5),
        ("XAU/USD", "Commodity", 0.01, 2),
        ("USOil", "Commodity", 0.01, 3),
    ):
        db.add(
            Asset(
                broker_id=1,
                symbol=symbol,
                category=category,
                point_size=point_size,
                digits=digits,
            ),
            context.instance,
        )


def insert_account_group(context: Context) -> None:
    """Insert the defined Account Group."""
    db.add(AccountGroup(user_id=1, name="Default"), context.instance)


def insert_account(context: Context) -> None:
    """Insert the defined Account with an encrypted generated password."""
    plain = context.plain["account"]
    db.add(
        Account(
            name=plain["name"],
            group_id=1,
            broker_id=1,
            instance_id=1,
            base_currency_id=1,
            username=plain["username"],
            password=credentials.encrypt(plain["password"], context.key),
            leverage=100,
            account_type="CFD",
        ),
        context.instance,
    )


def insert_trailing_group(context: Context) -> None:
    """Insert the defined Trailing Group."""
    db.add(TrailingGroup(user_id=1, name="Default"), context.instance)


def insert_partial_group(context: Context) -> None:
    """Insert the defined Partial Group."""
    db.add(PartialGroup(user_id=1, name="Default"), context.instance)


def insert_action_group(context: Context) -> None:
    """Insert the defined Action Group."""
    db.add(ActionGroup(user_id=1, name="Default"), context.instance)


def insert_action(context: Context) -> None:
    """Insert the defined Action."""
    action = Action(
        name="Default",
        action_group_id=1,
        asset_id=1,
        account_id=1,
        partial_group_id=1,
        trailing_group_id=1,
        risk_by_reward=Decimal(1),
        take_profit=Decimal(1),
        stop_loss=Decimal(1),
    )
    db.add(action, context.instance)


STEPS: dict[str, Callable[[Context], None]] = {
    "User": insert_user,
    "TradingPlatform": insert_trading_platforms,
    "Instance": insert_instance,
    "Currency": insert_currencies,
    "Broker": insert_broker,
    "Asset": insert_assets,
    "AccountGroup": insert_account_group,
    "Account": insert_account,
    "TrailingGroup": insert_trailing_group,
    "PartialGroup": insert_partial_group,
    "ActionGroup": insert_action_group,
    "Action": insert_action,
}


def run(instance: str | None = None, steps: Sequence[str] | None = None) -> Path:
    """Populate an Instance with the defined Initial Data.

    Args:
        instance (str, optional): Key of the Instance, or the default Instance when omitted.
        steps (Sequence[str], optional): Names of the steps to run, in order; every step when omitted.

    Returns:
        (Path): Owner-only file that holds the generated plaintext credentials.
    """
    if db.count(User, instance):
        raise RuntimeError(
            "The Instance already holds Initial Data; provision a fresh Instance first"
        )
    secrets_directory = data.current_configuration().root / ".secrets"
    context = Context(
        instance=instance,
        key=credentials.load_or_create_key(secrets_directory),
        plain={
            "user": {
                "username": "admin",
                "password": credentials.generate(),
                "api_key": credentials.generate(),
            },
            "instance": {
                "name": "MetaTrader",
                "password": credentials.generate(),
                "api_key": credentials.generate(),
            },
            "account": {
                "name": "Acc-1",
                "username": "test",
                "password": credentials.generate(),
            },
        },
    )
    delivered = credentials.deliver(context.plain, secrets_directory)
    for name in steps or STEPS:
        STEPS[name](context)
    return delivered


if __name__ == "__main__":
    print(f"Initial Data inserted. Generated credentials were written to {run()}")
