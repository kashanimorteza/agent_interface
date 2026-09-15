"""The repeatable Initial Data Seed/Import entry point.

Imports every Target-declared Initial Data record, in dependency order,
through the generic Database Interface, satisfying every relationship and
non-nullable field the Target declares. Repeatable: an already-present
logical record (matched by its declared natural key) is left untouched
rather than duplicated. Every "Generate securely" credential is generated
fresh only the first time its record is created.
"""

from __future__ import annotations

import secrets
from collections.abc import Callable, Mapping
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
    ModelBase,
    PartialGroup,
    TradingPlatform,
    TrailingGroup,
    User,
)

from database.interface import DatabaseInterface, Transaction

M_PLACEHOLDER_ID = 0


def _generate_secret() -> str:
    return secrets.token_urlsafe(32)


def _get_or_create[M: ModelBase](
    db: DatabaseInterface,
    model_cls: type[M],
    natural_key: Mapping[str, Any],
    build: Callable[[], M],
    *,
    txn: Transaction,
) -> M:
    existing = db.search(model_cls, natural_key, txn=txn)
    if existing:
        return existing[0]
    return db.create(build(), txn=txn)


def seed_initial_data(db: DatabaseInterface) -> User:
    """Import every Target-declared Initial Data record; safe to run repeatedly. Returns the seeded admin User."""
    with db.transaction() as txn:
        admin = _get_or_create(
            db,
            User,
            {"username": "admin"},
            lambda: User(
                id=M_PLACEHOLDER_ID,
                name="Admin",
                username="admin",
                password=_generate_secret(),
                api_key=_generate_secret(),
            ),
            txn=txn,
        )

        mt5 = _get_or_create(
            db,
            TradingPlatform,
            {"name": "MetaTrader 5"},
            lambda: TradingPlatform(
                id=M_PLACEHOLDER_ID, name="MetaTrader 5", code="metatrader_5"
            ),
            txn=txn,
        )
        _get_or_create(
            db,
            TradingPlatform,
            {"name": "Binance"},
            lambda: TradingPlatform(
                id=M_PLACEHOLDER_ID, name="Binance", code="binance"
            ),
            txn=txn,
        )

        instance = _get_or_create(
            db,
            Instance,
            {"user_id": admin.id, "name": "MetaTrader"},
            lambda: Instance(
                id=M_PLACEHOLDER_ID,
                user_id=admin.id,
                trading_platform_id=mt5.id,
                name="MetaTrader",
                ip="127.0.0.1",
                username="test",
                password=_generate_secret(),
                api_key=_generate_secret(),
            ),
            txn=txn,
        )

        currency_specs = [
            ("USD", "$", "United States", 2),
            ("EUR", "€", "Eurozone", 2),
            ("GBP", "£", "United Kingdom", 2),
            ("JPY", "¥", "Japan", 0),
            ("CHF", "CHF", "Switzerland", 2),
            ("CAD", "C$", "Canada", 2),
            ("AUD", "A$", "Australia", 2),
            ("NZD", "NZ$", "New Zealand", 2),
        ]
        currencies: dict[str, Currency] = {}
        for code, symbol, country, digits in currency_specs:
            currencies[code] = _get_or_create(
                db,
                Currency,
                {"user_id": admin.id, "code": code},
                lambda code=code, symbol=symbol, country=country, digits=digits: (
                    Currency(
                        id=M_PLACEHOLDER_ID,
                        user_id=admin.id,
                        code=code,
                        symbol=symbol,
                        country=country,
                        decimal_digits=digits,
                    )
                ),
                txn=txn,
            )

        broker = _get_or_create(
            db,
            Broker,
            {"user_id": admin.id, "name": "FxPro"},
            lambda: Broker(id=M_PLACEHOLDER_ID, name="FxPro", user_id=admin.id),
            txn=txn,
        )

        asset_specs = [
            ("EUR/USD", "Currency", 0.0001, 5),
            ("EUR/GBP", "Currency", 0.001, 5),
            ("XAU/USD", "Commodity", 0.01, 2),
            ("USOil", "Commodity", 0.01, 3),
        ]
        assets: dict[str, Asset] = {}
        for symbol, category, point_size, digits in asset_specs:
            assets[symbol] = _get_or_create(
                db,
                Asset,
                {"broker_id": broker.id, "symbol": symbol},
                lambda symbol=symbol, category=category, point_size=point_size, digits=digits: (
                    Asset(
                        id=M_PLACEHOLDER_ID,
                        broker_id=broker.id,
                        symbol=symbol,
                        category=category,
                        point_size=point_size,
                        digits=digits,
                    )
                ),
                txn=txn,
            )

        account_group = _get_or_create(
            db,
            AccountGroup,
            {"user_id": admin.id, "name": "Default"},
            lambda: AccountGroup(id=M_PLACEHOLDER_ID, user_id=admin.id, name="Default"),
            txn=txn,
        )

        account = _get_or_create(
            db,
            Account,
            {"name": "Acc-1"},
            lambda: Account(
                id=M_PLACEHOLDER_ID,
                name="Acc-1",
                group_id=account_group.id,
                broker_id=broker.id,
                instance_id=instance.id,
                base_currency_id=currencies["USD"].id,
                username="test",
                password=_generate_secret(),
                leverage=100,
                account_type="CFD",
            ),
            txn=txn,
        )

        trailing_group = _get_or_create(
            db,
            TrailingGroup,
            {"user_id": admin.id, "name": "Default"},
            lambda: TrailingGroup(
                id=M_PLACEHOLDER_ID, user_id=admin.id, name="Default"
            ),
            txn=txn,
        )

        partial_group = _get_or_create(
            db,
            PartialGroup,
            {"user_id": admin.id, "name": "Default"},
            lambda: PartialGroup(id=M_PLACEHOLDER_ID, user_id=admin.id, name="Default"),
            txn=txn,
        )

        action_group = _get_or_create(
            db,
            ActionGroup,
            {"user_id": admin.id, "name": "Default"},
            lambda: ActionGroup(id=M_PLACEHOLDER_ID, user_id=admin.id, name="Default"),
            txn=txn,
        )

        _get_or_create(
            db,
            Action,
            {"action_group_id": action_group.id, "name": "Default"},
            lambda: Action(
                id=M_PLACEHOLDER_ID,
                name="Default",
                action_group_id=action_group.id,
                asset_id=assets["EUR/USD"].id,
                account_id=account.id,
                partial_group_id=partial_group.id,
                trailing_group_id=trailing_group.id,
                risk_by_reward=Decimal(1),
                take_profit=Decimal(1),
                stop_loss=Decimal(1),
            ),
            txn=txn,
        )

    return admin
