"""Initial data — the resolved records of .interface/config/database.yaml, seeded idempotently by natural key."""

from __future__ import annotations

import secrets
from typing import Any

from sqlalchemy import MetaData, Table, and_, func, select
from sqlalchemy.engine import Connection

from my_database.data_logic.registry import get_model_by_table
from my_database.errors import CredentialKeyMissingError
from my_database.settings import get_settings
from my_database.storage_adapter.credentials import transform_for_storage


class _Generate:
    """Marker for a value the project asks to generate securely at seed time."""

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return "GENERATE"


GENERATE = _Generate()

# Ordered by dependency exactly as resolved in database.yaml data_logic.initial_data.records.
INITIAL_DATA: list[tuple[str, list[dict[str, Any]]]] = [
    ("users", [{"name": "Admin", "username": "admin", "password": GENERATE, "api_key": GENERATE}]),
    (
        "currencies",
        [
            {"name": "US Dollar", "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2},
            {"name": "Euro", "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
            {"name": "British Pound", "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2},
            {"name": "Japanese Yen", "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
            {"name": "Swiss Franc", "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2},
            {"name": "Canadian Dollar", "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
            {"name": "Australian Dollar", "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
            {"name": "New Zealand Dollar", "code": "NZD", "symbol": "NZ$", "country": "New Zealand", "decimal_digits": 2},
        ],
    ),
    ("trading_platforms", [{"name": "MetaTrader 5", "code": "metatrader_5"}, {"name": "Binance", "code": "binance"}]),
    ("brokers", [{"name": "FxPro", "user_id": 1, "trading_platform_id": 1}]),
    (
        "accounts",
        [
            {
                "name": "Acc-1",
                "broker_id": 1,
                "base_currency_id": 1,
                "username": "test",
                "password": GENERATE,
                "leverage": 100,
                "account_type": "CFD",
            }
        ],
    ),
    (
        "assets",
        [
            {"name": "EURUSD", "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
            {"name": "EURGBP", "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
            {"name": "XAUUSD", "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
            {"name": "USOil", "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
        ],
    ),
    ("trailing_groups", [{"name": "Default"}]),
    ("partial_groups", [{"name": "Default"}]),
    ("action_groups", [{"name": "Default"}]),
    (
        "actions",
        [
            {
                "name": "Default",
                "action_group_id": 1,
                "asset_id": 1,
                "account_id": 1,
                "partial_group_id": 1,
                "trailing_group_id": 1,
                "risk_by_reward": 1,
                "take_profit": 1,
                "stop_loss": 1,
            }
        ],
    ),
]

NATURAL_KEYS: dict[str, tuple[str, ...]] = {
    "users": ("name",),
    "currencies": ("code",),
    "trading_platforms": ("name",),
    "brokers": ("user_id", "name"),
    "accounts": ("name",),
    "assets": ("symbol",),
    "trailing_groups": ("name",),
    "partial_groups": ("name",),
    "action_groups": ("name",),
    "actions": ("name",),
}


def _reflect(connection: Connection, name: str) -> Table:
    return Table(name, MetaData(), autoload_with=connection)


def _key_clause(table: Table, record: dict[str, Any]):
    return and_(*(table.c[k] == record[k] for k in NATURAL_KEYS[table.name]))


def _exists(connection: Connection, table: Table, record: dict[str, Any]) -> bool:
    return connection.execute(select(func.count()).select_from(table).where(_key_clause(table, record))).scalar() > 0


def _require_key_if_needed() -> None:
    needs_key = any(
        get_model_by_table(table).credential_fields.get(field) == "encrypted"
        for table, records in INITIAL_DATA
        for record in records
        for field in record
    )
    if needs_key and not get_settings().credential_encryption_key:
        raise CredentialKeyMissingError(
            "CREDENTIAL_ENCRYPTION_KEY is required to seed encrypted credential fields; nothing was written"
        )


def seed(connection: Connection) -> dict[str, int]:
    """Insert every initial record whose natural key is absent; return inserted counts per table."""
    _require_key_if_needed()
    inserted: dict[str, int] = {}
    for table_name, records in INITIAL_DATA:
        table = _reflect(connection, table_name)
        modes = get_model_by_table(table_name).credential_fields
        count = 0
        for record in records:
            if _exists(connection, table, record):
                continue
            row: dict[str, Any] = {}
            natural = "-".join(str(record[k]) for k in NATURAL_KEYS[table_name])
            for field, value in record.items():
                if value is GENERATE:
                    value = secrets.token_urlsafe(32)
                    print(f"GENERATED CREDENTIAL {table_name}.{natural}.{field}: {value}", flush=True)
                if field in modes:
                    value = transform_for_storage(value, modes[field])
                row[field] = value
            connection.execute(table.insert().values(**row))
            count += 1
        inserted[table_name] = count
    return inserted


def unseed(connection: Connection) -> dict[str, int]:
    """Delete every initial record matched by natural key, in reverse dependency order."""
    removed: dict[str, int] = {}
    for table_name, records in reversed(INITIAL_DATA):
        table = _reflect(connection, table_name)
        count = 0
        for record in records:
            count += connection.execute(table.delete().where(_key_clause(table, record))).rowcount
        removed[table_name] = count
    return removed
