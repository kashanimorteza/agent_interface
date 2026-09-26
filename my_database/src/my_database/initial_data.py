"""Initial Data: the records the Target defines, inserted into the default Database Instance."""

from decimal import Decimal

import my_model.interface as model
from sqlmodel import SQLModel

from my_database.configuration import Configuration
from my_database.credentials import generate_credential
from my_database.interface import Interface


class InitialDataError(Exception):
    """Raised when an initial record cannot be stored or would not receive the identifier the Target assumes."""


class InitialData:
    """Inserts each Entity's Initial Data, in the order the Target lists it, into an empty Table.

    Attributes:
        interface (Interface): The Interface through which every record is added and protected.
        generated (dict[str, dict[str, str]]): Plain credential values generated during this run, by Entity name; held in memory only.
    """

    def __init__(self, interface: Interface):
        """Prepare insertion through an Interface.

        Args:
            interface (Interface): Interface whose default Database Instance receives the records.
        """
        self.interface = interface
        self.generated: dict[str, dict[str, str]] = {}

    def _insert(self, entity: type[SQLModel], records: list[SQLModel]) -> bool:
        """Add records to an empty Table so each receives the identifier the Target's references assume.

        Args:
            entity (type[SQLModel]): Entity class of the records.
            records (list[SQLModel]): Records in the order the Target lists them.

        Returns:
            (bool): True when inserted; False when the Table already holds records and was left untouched.
        """
        if self.interface.list_(entity).value:
            return False
        for expected_id, record in enumerate(records, start=1):
            result = self.interface.add(record)
            if not result.ok or getattr(result.value, "id", None) != expected_id:
                raise InitialDataError(
                    f"{entity.__name__} record {expected_id} was not stored as expected: {result.message}"
                )
        return True

    def users(self) -> bool:
        """Insert the initial User records; the plain generated credentials stay in memory under 'User'."""
        password, api_key = generate_credential(), generate_credential()
        inserted = self._insert(
            model.User,
            [
                model.User(
                    name="Admin", username="admin", password=password, api_key=api_key
                )
            ],
        )
        if inserted:
            self.generated["User"] = {
                "username": "admin",
                "password": password,
                "api_key": api_key,
            }
        return inserted

    def trading_platforms(self) -> bool:
        """Insert the initial Trading Platform records."""
        return self._insert(
            model.TradingPlatform,
            [
                model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"),
                model.TradingPlatform(name="Binance", code="binance"),
            ],
        )

    def instances(self) -> bool:
        """Insert the initial Instance records; their credentials are generated and stored encrypted."""
        return self._insert(
            model.Instance,
            [
                model.Instance(
                    name="MetaTrader",
                    user_id=1,
                    trading_platform_id=1,
                    ip="127.0.0.1",
                    username="test",
                    password=generate_credential(),
                    api_key=generate_credential(),
                )
            ],
        )

    def currencies(self) -> bool:
        """Insert the initial Currency records."""
        rows = [
            ("USD", "$", "United States", 2),
            ("EUR", "€", "Eurozone", 2),
            ("GBP", "£", "United Kingdom", 2),
            ("JPY", "¥", "Japan", 0),
            ("CHF", "CHF", "Switzerland", 2),
            ("CAD", "C$", "Canada", 2),
            ("AUD", "A$", "Australia", 2),
            ("NZD", "NZ$", "New Zealand", 2),
        ]
        return self._insert(
            model.Currency,
            [
                model.Currency(
                    user_id=1,
                    code=code,
                    symbol=symbol,
                    country=country,
                    decimal_digits=digits,
                )
                for code, symbol, country, digits in rows
            ],
        )

    def brokers(self) -> bool:
        """Insert the initial Broker records."""
        return self._insert(model.Broker, [model.Broker(name="FxPro", user_id=1)])

    def account_groups(self) -> bool:
        """Insert the initial Account Group records."""
        return self._insert(
            model.AccountGroup, [model.AccountGroup(user_id=1, name="Default")]
        )

    def assets(self) -> bool:
        """Insert the initial Asset records."""
        rows = [
            ("EUR/USD", "Currency", 0.0001, 5),
            ("EUR/GBP", "Currency", 0.001, 5),
            ("XAU/USD", "Commodity", 0.01, 2),
            ("USOil", "Commodity", 0.01, 3),
        ]
        return self._insert(
            model.Asset,
            [
                model.Asset(
                    broker_id=1,
                    symbol=symbol,
                    category=category,
                    point_size=point_size,
                    digits=digits,
                )
                for symbol, category, point_size, digits in rows
            ],
        )

    def accounts(self) -> bool:
        """Insert the initial Account records; their credential is generated and stored encrypted."""
        return self._insert(
            model.Account,
            [
                model.Account(
                    name="Acc-1",
                    group_id=1,
                    broker_id=1,
                    instance_id=1,
                    base_currency_id=1,
                    username="test",
                    password=generate_credential(),
                    leverage=100,
                    account_type="CFD",
                )
            ],
        )

    def trailing_groups(self) -> bool:
        """Insert the initial Trailing Group records."""
        return self._insert(
            model.TrailingGroup, [model.TrailingGroup(user_id=1, name="Default")]
        )

    def partial_groups(self) -> bool:
        """Insert the initial Partial Group records."""
        return self._insert(
            model.PartialGroup, [model.PartialGroup(user_id=1, name="Default")]
        )

    def action_groups(self) -> bool:
        """Insert the initial Action Group records."""
        return self._insert(
            model.ActionGroup, [model.ActionGroup(user_id=1, name="Default")]
        )

    def actions(self) -> bool:
        """Insert the initial Action records."""
        return self._insert(
            model.Action,
            [
                model.Action(
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
            ],
        )

    def load(self) -> dict[str, dict[str, str]]:
        """Insert every Entity's Initial Data in dependency order.

        Returns:
            (dict[str, dict[str, str]]): Plain credentials generated for the User during this run; empty when nothing was inserted.
        """
        self.users()
        self.trading_platforms()
        self.instances()
        self.currencies()
        self.brokers()
        self.assets()
        self.account_groups()
        self.accounts()
        self.trailing_groups()
        self.partial_groups()
        self.action_groups()
        self.actions()
        return self.generated


if __name__ == "__main__":
    data = InitialData(Interface(Configuration.load()))
    try:
        data.load()
    finally:  # generated credentials are unrecoverable once hashed, so print them even when a later step fails
        for name, values in data.generated.items():
            print(
                f"Generated {name} credentials (shown once, not stored in plain form): {values}"
            )
