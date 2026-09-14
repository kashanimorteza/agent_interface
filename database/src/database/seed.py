"""Seeds every Target-declared initial record, in dependency order, repeatably."""

from __future__ import annotations

import secrets
from typing import Any

import model

from .db_interface import Database


def _generate_secret() -> str:
    return secrets.token_urlsafe(32)


def _get_or_create[ModelT: model.ModelBase](
    db: Database, model_cls: type[ModelT], defaults: dict[str, Any], **natural_key: Any
) -> ModelT:
    existing = db.list(model_cls, **natural_key)
    if existing:
        return existing[0]
    return db.create(model_cls(**natural_key, **defaults))


def seed_initial_data(db: Database) -> None:
    """Seed every Target-declared initial record. Safe to call more than once."""
    admin = _get_or_create(
        db,
        model.User,
        {
            "username": "admin",
            "password": _generate_secret(),
            "api_key": _generate_secret(),
        },
        name="Admin",
    )

    mt5 = _get_or_create(db, model.TradingPlatform, {}, name="MetaTrader 5", code="metatrader_5")
    _get_or_create(db, model.TradingPlatform, {}, name="Binance", code="binance")

    instance = _get_or_create(
        db,
        model.Instance,
        {
            "trading_platform_id": mt5.id,
            "ip": "127.0.0.1",
            "username": "test",
            "password": _generate_secret(),
            "api_key": _generate_secret(),
        },
        user_id=admin.id,
        name="MetaTrader",
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
    currency_by_code: dict[str, model.Currency] = {}
    for code, symbol, country, decimal_digits in currencies:
        currency_by_code[code] = _get_or_create(
            db,
            model.Currency,
            {"symbol": symbol, "country": country, "decimal_digits": decimal_digits},
            user_id=admin.id,
            code=code,
        )

    broker = _get_or_create(db, model.Broker, {}, name="FxPro", user_id=admin.id)

    assets = [
        ("EUR/USD", "Currency", 0.0001, 5),
        ("EUR/GBP", "Currency", 0.001, 5),
        ("XAU/USD", "Commodity", 0.01, 2),
        ("USOil", "Commodity", 0.01, 3),
    ]
    asset_by_symbol: dict[str, model.Asset] = {}
    for symbol, category, point_size, digits in assets:
        asset_by_symbol[symbol] = _get_or_create(
            db,
            model.Asset,
            {"category": category, "point_size": point_size, "digits": digits},
            broker_id=broker.id,
            symbol=symbol,
        )

    account_group = _get_or_create(db, model.AccountGroup, {}, name="Default", user_id=admin.id)

    account = _get_or_create(
        db,
        model.Account,
        {
            "group_id": account_group.id,
            "broker_id": broker.id,
            "instance_id": instance.id,
            "base_currency_id": currency_by_code["USD"].id,
            "username": "test",
            "password": _generate_secret(),
            "leverage": 100,
            "account_type": "CFD",
        },
        name="Acc-1",
    )

    trailing_group = _get_or_create(db, model.TrailingGroup, {}, name="Default", user_id=admin.id)
    partial_group = _get_or_create(db, model.PartialGroup, {}, name="Default", user_id=admin.id)
    action_group = _get_or_create(db, model.ActionGroup, {}, name="Default", user_id=admin.id)

    _get_or_create(
        db,
        model.Action,
        {
            "asset_id": asset_by_symbol["EUR/USD"].id,
            "account_id": account.id,
            "partial_group_id": partial_group.id,
            "trailing_group_id": trailing_group.id,
            "risk_by_reward": 1,
            "take_profit": 1,
            "stop_loss": 1,
        },
        action_group_id=action_group.id,
        name="Default",
    )
