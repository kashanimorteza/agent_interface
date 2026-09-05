"""The project's initial records, copied exactly from the generated Database configuration.

``GENERATE`` marks a value the project says to generate securely; it is fulfilled
at seed time and the plain value is never written here or persisted.
"""

from __future__ import annotations


class _Generate:
    __slots__ = ()

    def __repr__(self) -> str:
        return "GENERATE"


GENERATE = _Generate()

# (model_key, natural_key, records) in dependency order.
SEED: list[tuple[str, tuple[str, ...], list[dict]]] = [
    ("user", ("name",), [
        {"name": "Admin", "username": "admin", "password": GENERATE, "api_key": GENERATE},
    ]),
    ("currency", ("code",), [
        {"name": "US Dollar", "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2},
        {"name": "Euro", "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
        {"name": "British Pound", "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2},
        {"name": "Japanese Yen", "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
        {"name": "Swiss Franc", "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2},
        {"name": "Canadian Dollar", "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
        {"name": "Australian Dollar", "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
        {"name": "New Zealand Dollar", "code": "NZD", "symbol": "NZ$", "country": "New Zealand", "decimal_digits": 2},
    ]),
    ("trading_platform", ("name",), [
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    ]),
    ("broker", ("user_id", "name"), [
        {"name": "FxPro", "user_id": 1, "trading_platform_id": 1},
    ]),
    ("account", ("name",), [
        {"name": "Acc-1", "broker_id": 1, "base_currency_id": 1, "username": "test", "password": GENERATE, "leverage": 100, "account_type": "CFD"},
    ]),
    ("asset", ("symbol",), [
        {"name": "EURUSD", "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
        {"name": "EURGBP", "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
        {"name": "XAUUSD", "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
        {"name": "USOil", "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
    ]),
    ("trailing_group", ("name",), [{"name": "Default"}]),
    ("partial_group", ("name",), [{"name": "Default"}]),
    ("action_group", ("name",), [{"name": "Default"}]),
    ("action", ("name",), [
        {"name": "Default", "action_group_id": 1, "asset_id": 1, "account_id": 1, "partial_group_id": 1, "trailing_group_id": 1,
         "risk_by_reward": 1, "take_profit": 1, "stop_loss": 1},
    ]),
]
