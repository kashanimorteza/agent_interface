"""Initial Data import.

Imports every Target-declared Initial Data record, in dependency order,
through the generic Database Interface, generating a secure value for any
field the Target marks as generated and surfacing it to the operator exactly
once outside any log, backup, or export. Repeatable: an already-present
logical record (identified by the Model's own declared unique identity) is
left untouched.
"""

from __future__ import annotations

import secrets
from decimal import Decimal
from typing import Any

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
from model.foundation import DomainModel

from database.interface import Transaction, create, search


def _generate_secret() -> str:
    return secrets.token_urlsafe(32)


def _print_generated(model: type[DomainModel], field: str, identity: str, value: str) -> None:
    print(f"Generated {model.__name__}.{field} for '{identity}': {value}")  # noqa: T201


def _find_one(model: type[DomainModel], tx: Transaction, **criteria: Any) -> DomainModel | None:
    matches = search(model, tx=tx, **criteria)
    return matches[0] if matches else None


def import_initial_data(*, instance: str | None = None) -> None:
    from database.interface import transaction

    with transaction(instance=instance) as tx:
        # 1. User
        admin = _find_one(User, tx, username="admin")
        if admin is None:
            password = _generate_secret()
            api_key = _generate_secret()
            admin = create(
                User,
                tx=tx,
                name="Admin",
                username="admin",
                password=password,
                api_key=api_key,
            )
            _print_generated(User, "password", "admin", password)
            _print_generated(User, "api_key", "admin", api_key)

        # 2. Trading Platform
        platforms: dict[str, Any] = {}
        for name, code in (("MetaTrader 5", "metatrader_5"), ("Binance", "binance")):
            platform = _find_one(TradingPlatform, tx, code=code)
            if platform is None:
                platform = create(TradingPlatform, tx=tx, name=name, code=code)
            platforms[code] = platform

        # 3. Broker
        broker = _find_one(Broker, tx, user_id=admin.id, name="FxPro")
        if broker is None:
            broker = create(Broker, tx=tx, name="FxPro", user_id=admin.id)

        # 4. Currency
        currency_rows = [
            ("USD", "$", "United States", 2),
            ("EUR", "€", "Eurozone", 2),
            ("GBP", "£", "United Kingdom", 2),
            ("JPY", "¥", "Japan", 0),
            ("CHF", "CHF", "Switzerland", 2),
            ("CAD", "C$", "Canada", 2),
            ("AUD", "A$", "Australia", 2),
            ("NZD", "NZ$", "New Zealand", 2),
        ]
        currencies: dict[str, Any] = {}
        for code, symbol, country, digits in currency_rows:
            currency = _find_one(Currency, tx, user_id=admin.id, code=code)
            if currency is None:
                currency = create(
                    Currency,
                    tx=tx,
                    user_id=admin.id,
                    code=code,
                    symbol=symbol,
                    country=country,
                    decimal_digits=digits,
                )
            currencies[code] = currency

        # 5. Instance
        instance_row = _find_one(Instance, tx, user_id=admin.id, name="MetaTrader")
        if instance_row is None:
            inst_password = _generate_secret()
            inst_api_key = _generate_secret()
            instance_row = create(
                Instance,
                tx=tx,
                user_id=admin.id,
                trading_platform_id=platforms["metatrader_5"].id,
                name="MetaTrader",
                ip="127.0.0.1",
                username="test",
                password=inst_password,
                api_key=inst_api_key,
            )
            _print_generated(Instance, "password", "MetaTrader", inst_password)
            _print_generated(Instance, "api_key", "MetaTrader", inst_api_key)

        # 6. Account Group
        account_group = _find_one(AccountGroup, tx, user_id=admin.id, name="Default")
        if account_group is None:
            account_group = create(AccountGroup, tx=tx, user_id=admin.id, name="Default")

        # 7. Asset
        asset_rows = [
            ("EUR/USD", "Currency", 0.0001, 5),
            ("EUR/GBP", "Currency", 0.001, 5),
            ("XAU/USD", "Commodity", 0.01, 2),
            ("USOil", "Commodity", 0.01, 3),
        ]
        assets: dict[str, Any] = {}
        for symbol, category, point_size, digits in asset_rows:
            asset = _find_one(Asset, tx, broker_id=broker.id, symbol=symbol)
            if asset is None:
                asset = create(
                    Asset,
                    tx=tx,
                    broker_id=broker.id,
                    symbol=symbol,
                    category=category,
                    point_size=point_size,
                    digits=digits,
                )
            assets[symbol] = asset

        # 8. Account
        account = _find_one(Account, tx, name="Acc-1")
        if account is None:
            acc_password = _generate_secret()
            account = create(
                Account,
                tx=tx,
                name="Acc-1",
                group_id=account_group.id,
                broker_id=broker.id,
                instance_id=instance_row.id,
                base_currency_id=currencies["USD"].id,
                username="test",
                password=acc_password,
                leverage=100,
                account_type="CFD",
            )
            _print_generated(Account, "password", "Acc-1", acc_password)

        # 9. Trailing Group
        trailing_group = _find_one(TrailingGroup, tx, user_id=admin.id, name="Default")
        if trailing_group is None:
            trailing_group = create(TrailingGroup, tx=tx, user_id=admin.id, name="Default")

        # 10. Partial Group
        partial_group = _find_one(PartialGroup, tx, user_id=admin.id, name="Default")
        if partial_group is None:
            partial_group = create(PartialGroup, tx=tx, user_id=admin.id, name="Default")

        # 11. Action Group
        action_group = _find_one(ActionGroup, tx, user_id=admin.id, name="Default")
        if action_group is None:
            action_group = create(ActionGroup, tx=tx, user_id=admin.id, name="Default")

        # 12. Action
        action = _find_one(Action, tx, action_group_id=action_group.id, name="Default")
        if action is None:
            create(
                Action,
                tx=tx,
                name="Default",
                action_group_id=action_group.id,
                asset_id=assets["EUR/USD"].id,
                account_id=account.id,
                partial_group_id=partial_group.id,
                trailing_group_id=trailing_group.id,
                risk_by_reward=Decimal("1"),
                take_profit=Decimal("1"),
                stop_loss=Decimal("1"),
            )

        # TrailingRule, PartialRule, and Position declare no Initial Data in the
        # Target and are intentionally not seeded here.
