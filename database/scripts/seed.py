#!/usr/bin/env python3
"""The reusable, repeatable Seed/Import entry point (Database Principle 13, Database Preferences
`settings.data_logic.initial_data`): imports every Target-declared Initial Data record in
dependency order. Repeatable without creating duplicate logical records — each record is looked
up by its Target-declared natural/unique key before being created.

Run: `uv run python scripts/seed.py`
"""

from __future__ import annotations

import secrets
import sys

import model
from database import DatabaseInterface, Transaction


def _generate_secret() -> str:
    """A securely generated credential value for a Target field declared 'Generate securely'.
    Printed once to stdout at seed time so an operator can capture it — never persisted in a
    file, log, or Interface record (Database Principle 12)."""
    return secrets.token_urlsafe(32)


def _get_or_create(
    db: DatabaseInterface,
    tx: Transaction,
    model_cls: type[model.ModelFoundation],
    *,
    lookup: dict[str, object],
    build: dict[str, object],
) -> model.ModelFoundation:
    existing = db.search(model_cls, transaction=tx, **lookup)
    if existing:
        return existing[0]
    return db.create(model_cls(**build), transaction=tx)


def seed(db: DatabaseInterface) -> list[str]:
    """Seed every Target-declared Initial Data record. Returns the plaintext of any newly
    generated secure credential, for the caller to print once."""
    generated_secrets: list[str] = []

    with db.transaction() as tx:
        user_password = _generate_secret()
        user_api_key = _generate_secret()
        admin = _get_or_create(
            db,
            tx,
            model.User,
            lookup={"name": "Admin"},
            build={
                "name": "Admin",
                "username": "admin",
                "password": user_password,
                "api_key": user_api_key,
            },
        )
        if admin.password == user_password:  # freshly created this run
            generated_secrets += [
                f"User 'Admin' password: {user_password}",
                f"User 'Admin' api_key: {user_api_key}",
            ]

        metatrader_5 = _get_or_create(
            db,
            tx,
            model.TradingPlatform,
            lookup={"code": "metatrader_5"},
            build={"name": "MetaTrader 5", "code": "metatrader_5"},
        )
        _get_or_create(
            db,
            tx,
            model.TradingPlatform,
            lookup={"code": "binance"},
            build={"name": "Binance", "code": "binance"},
        )

        broker = _get_or_create(
            db,
            tx,
            model.Broker,
            lookup={"user_id": admin.id, "name": "FxPro"},
            build={"name": "FxPro", "user_id": admin.id},
        )

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
        currencies: dict[str, model.Currency] = {}
        for code, symbol, country, decimal_digits in currency_rows:
            currencies[code] = _get_or_create(
                db,
                tx,
                model.Currency,
                lookup={"user_id": admin.id, "code": code},
                build={
                    "user_id": admin.id,
                    "code": code,
                    "symbol": symbol,
                    "country": country,
                    "decimal_digits": decimal_digits,
                },
            )

        account_group = _get_or_create(
            db,
            tx,
            model.AccountGroup,
            lookup={"user_id": admin.id, "name": "Default"},
            build={"user_id": admin.id, "name": "Default"},
        )
        trailing_group = _get_or_create(
            db,
            tx,
            model.TrailingGroup,
            lookup={"user_id": admin.id, "name": "Default"},
            build={"user_id": admin.id, "name": "Default"},
        )
        partial_group = _get_or_create(
            db,
            tx,
            model.PartialGroup,
            lookup={"user_id": admin.id, "name": "Default"},
            build={"user_id": admin.id, "name": "Default"},
        )
        action_group = _get_or_create(
            db,
            tx,
            model.ActionGroup,
            lookup={"user_id": admin.id, "name": "Default"},
            build={"user_id": admin.id, "name": "Default"},
        )

        instance_password = _generate_secret()
        instance_api_key = _generate_secret()
        instance = _get_or_create(
            db,
            tx,
            model.Instance,
            lookup={"user_id": admin.id, "name": "MetaTrader"},
            build={
                "user_id": admin.id,
                "name": "MetaTrader",
                "trading_platform_id": metatrader_5.id,
                "ip": "127.0.0.1",
                "username": "test",
                "password": instance_password,
                "api_key": instance_api_key,
            },
        )
        if instance.password == instance_password:
            generated_secrets += [
                f"Instance 'MetaTrader' password: {instance_password}",
                f"Instance 'MetaTrader' api_key: {instance_api_key}",
            ]

        asset_rows = [
            ("EUR/USD", "Currency", 0.0001, 5),
            ("EUR/GBP", "Currency", 0.001, 5),
            ("XAU/USD", "Commodity", 0.01, 2),
            ("USOil", "Commodity", 0.01, 3),
        ]
        assets: dict[str, model.Asset] = {}
        for symbol, category, point_size, digits in asset_rows:
            assets[symbol] = _get_or_create(
                db,
                tx,
                model.Asset,
                lookup={"broker_id": broker.id, "symbol": symbol},
                build={
                    "broker_id": broker.id,
                    "symbol": symbol,
                    "category": category,
                    "point_size": point_size,
                    "digits": digits,
                },
            )

        account_password = _generate_secret()
        account = _get_or_create(
            db,
            tx,
            model.Account,
            lookup={"name": "Acc-1"},
            build={
                "name": "Acc-1",
                "group_id": account_group.id,
                "broker_id": broker.id,
                "instance_id": instance.id,
                "base_currency_id": currencies["USD"].id,
                "username": "test",
                "password": account_password,
                "leverage": 100,
                "account_type": "CFD",
            },
        )
        if account.password == account_password:
            generated_secrets.append(f"Account 'Acc-1' password: {account_password}")

        _get_or_create(
            db,
            tx,
            model.Action,
            lookup={"action_group_id": action_group.id, "name": "Default"},
            build={
                "name": "Default",
                "action_group_id": action_group.id,
                "asset_id": assets["EUR/USD"].id,
                "account_id": account.id,
                "partial_group_id": partial_group.id,
                "trailing_group_id": trailing_group.id,
                "risk_by_reward": 1,
                "take_profit": 1,
                "stop_loss": 1,
            },
        )

    return generated_secrets


def main() -> int:
    db = DatabaseInterface()
    generated = seed(db)
    if generated:
        print("Generated secure credentials (shown once, not stored anywhere as plaintext):")
        for line in generated:
            print(f"  {line}")
    else:
        print("Initial data already present; nothing new was seeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
