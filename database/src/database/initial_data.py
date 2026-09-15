"""Imports the Target-declared initial data in dependency order.

Repeatable: re-running resolves each record by its natural key and leaves an
already-imported logical record untouched rather than duplicating it.
"""

from __future__ import annotations

import secrets
from collections.abc import Callable
from dataclasses import dataclass
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

from database import interface as db


def _secure_token() -> str:
    return secrets.token_urlsafe(32)


@dataclass(frozen=True)
class InitialRecord:
    """One Target-declared initial record: how to find it, and how to build it."""

    ref: str
    model_cls: type[DomainModel]
    natural_key: tuple[str, ...]
    build: Callable[[dict[str, int]], dict[str, Any]]


INITIAL_RECORDS: tuple[InitialRecord, ...] = (
    InitialRecord(
        "user.admin",
        User,
        ("username",),
        lambda refs: {
            "name": "Admin",
            "username": "admin",
            "password": _secure_token(),
            "api_key": _secure_token(),
        },
    ),
    InitialRecord(
        "platform.metatrader5",
        TradingPlatform,
        ("code",),
        lambda refs: {"name": "MetaTrader 5", "code": "metatrader_5"},
    ),
    InitialRecord(
        "platform.binance",
        TradingPlatform,
        ("code",),
        lambda refs: {"name": "Binance", "code": "binance"},
    ),
    InitialRecord(
        "instance.metatrader",
        Instance,
        ("user_id", "name"),
        lambda refs: {
            "user_id": refs["user.admin"],
            "trading_platform_id": refs["platform.metatrader5"],
            "name": "MetaTrader",
            "ip": "127.0.0.1",
            "username": "test",
            "password": _secure_token(),
            "api_key": _secure_token(),
        },
    ),
    *(
        InitialRecord(
            f"currency.{code.lower()}",
            Currency,
            ("user_id", "code"),
            lambda refs, code=code, symbol=symbol, country=country, digits=digits: {
                "user_id": refs["user.admin"],
                "code": code,
                "symbol": symbol,
                "country": country,
                "decimal_digits": digits,
            },
        )
        for code, symbol, country, digits in (
            ("USD", "$", "United States", 2),
            ("EUR", "€", "Eurozone", 2),
            ("GBP", "£", "United Kingdom", 2),
            ("JPY", "¥", "Japan", 0),
            ("CHF", "CHF", "Switzerland", 2),
            ("CAD", "C$", "Canada", 2),
            ("AUD", "A$", "Australia", 2),
            ("NZD", "NZ$", "New Zealand", 2),
        )
    ),
    InitialRecord(
        "broker.fxpro",
        Broker,
        ("user_id", "name"),
        lambda refs: {"name": "FxPro", "user_id": refs["user.admin"]},
    ),
    *(
        InitialRecord(
            f"asset.{symbol.replace('/', '').lower()}",
            Asset,
            ("broker_id", "symbol"),
            lambda refs, symbol=symbol, category=category, point_size=point_size, digits=digits: {
                "broker_id": refs["broker.fxpro"],
                "symbol": symbol,
                "category": category,
                "point_size": point_size,
                "digits": digits,
            },
        )
        for symbol, category, point_size, digits in (
            ("EUR/USD", "Currency", 0.0001, 5),
            ("EUR/GBP", "Currency", 0.001, 5),
            ("XAU/USD", "Commodity", 0.01, 2),
            ("USOil", "Commodity", 0.01, 3),
        )
    ),
    InitialRecord(
        "account_group.default",
        AccountGroup,
        ("user_id", "name"),
        lambda refs: {"user_id": refs["user.admin"], "name": "Default"},
    ),
    InitialRecord(
        "account.acc1",
        Account,
        ("group_id", "broker_id", "instance_id"),
        lambda refs: {
            "name": "Acc-1",
            "group_id": refs["account_group.default"],
            "broker_id": refs["broker.fxpro"],
            "instance_id": refs["instance.metatrader"],
            "base_currency_id": refs["currency.usd"],
            "username": "test",
            "password": _secure_token(),
            "leverage": 100,
            "account_type": "CFD",
        },
    ),
    InitialRecord(
        "trailing_group.default",
        TrailingGroup,
        ("user_id", "name"),
        lambda refs: {"user_id": refs["user.admin"], "name": "Default"},
    ),
    InitialRecord(
        "partial_group.default",
        PartialGroup,
        ("user_id", "name"),
        lambda refs: {"user_id": refs["user.admin"], "name": "Default"},
    ),
    InitialRecord(
        "action_group.default",
        ActionGroup,
        ("user_id", "name"),
        lambda refs: {"user_id": refs["user.admin"], "name": "Default"},
    ),
    InitialRecord(
        "action.default",
        Action,
        ("action_group_id", "name"),
        lambda refs: {
            "name": "Default",
            "action_group_id": refs["action_group.default"],
            "asset_id": refs["asset.eurusd"],
            "account_id": refs["account.acc1"],
            "partial_group_id": refs["partial_group.default"],
            "trailing_group_id": refs["trailing_group.default"],
            "risk_by_reward": 1,
            "take_profit": 1,
            "stop_loss": 1,
        },
    ),
)


def import_initial_data(instance_key: str | None = None) -> dict[str, int]:
    """Import every declared initial record, resolving dependencies in order.

    Returns the resolved id of every record, keyed by its stable reference name.
    Safe to run repeatedly: an already-imported logical record is found by its
    natural key and reused rather than duplicated.
    """
    refs: dict[str, int] = {}
    with db.transaction(instance_key) as session:
        for record in INITIAL_RECORDS:
            values = record.build(refs)
            key_criteria = {field: values[field] for field in record.natural_key}
            existing = session.search(record.model_cls, **key_criteria)
            if existing:
                refs[record.ref] = existing[0].id  # type: ignore[assignment]
                continue
            created = session.create(record.model_cls(**values))
            refs[record.ref] = created.id  # type: ignore[assignment]
    return refs
