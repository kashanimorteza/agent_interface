"""Initial data declared by the project definition.

Revision ID: 0002_initial_data
Revises: 0001_schema
Create Date: 2026-09-07

Applied idempotently: each record is matched on its Model's natural key, so
re-running inserts nothing that already exists. A credential written as
GENERATE is fulfilled with a cryptographically random value at seed time (the
value is reported once on standard error and never stored in clear). The
downgrade removes the records matching these natural keys.
"""
import sys

from alembic import op
from my_model import Account, AccountGroup, Action, ActionGroup, Asset, Broker, Currency, PartialGroup, TradingPlatform, TrailingGroup, User

from my_database.data_logic.seeding import GENERATE, Seed, apply, remove, requires_key
from my_database.storage_adapter import credential_key

revision = "0002_initial_data"
down_revision = "0001_schema"
branch_labels = None
depends_on = None

SEEDS = (
    Seed(User, ("name",), (
        {"name": "Admin", "username": "admin", "password": GENERATE, "api_key": GENERATE},
    )),
    Seed(Currency, ("code",), (
        {"name": "US Dollar", "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2},
        {"name": "Euro", "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
        {"name": "British Pound", "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2},
        {"name": "Japanese Yen", "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
        {"name": "Swiss Franc", "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2},
        {"name": "Canadian Dollar", "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
        {"name": "Australian Dollar", "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
        {"name": "New Zealand Dollar", "code": "NZD", "symbol": "NZ$", "country": "New Zealand", "decimal_digits": 2},
    )),
    Seed(TradingPlatform, ("name",), (
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    )),
    Seed(Broker, ("user_id", "name"), (
        {"name": "FxPro", "user_id": 1, "trading_platform_id": 1},
    )),
    Seed(AccountGroup, ("name",), (
        {"name": "Default"},
    )),
    Seed(Account, ("name",), (
        {"name": "Acc-1", "group_id": 1, "broker_id": 1, "base_currency_id": 1, "username": "test", "password": GENERATE, "leverage": 100, "account_type": "CFD"},
    )),
    Seed(Asset, ("symbol",), (
        {"name": "EURUSD", "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
        {"name": "EURGBP", "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
        {"name": "XAUUSD", "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
        {"name": "USOil", "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
    )),
    Seed(TrailingGroup, ("name",), (
        {"name": "Default"},
    )),
    Seed(PartialGroup, ("name",), (
        {"name": "Default"},
    )),
    Seed(ActionGroup, ("name",), (
        {"name": "Default"},
    )),
    Seed(Action, ("name",), (
        {"name": "Default", "action_group_id": 1, "asset_id": 1, "account_id": 1, "partial_group_id": 1, "trailing_group_id": 1, "risk_by_reward": 1, "take_profit": 1, "stop_loss": 1},
    )),
)


def upgrade() -> None:
    key = credential_key() if requires_key(SEEDS) else ""
    apply(op.get_bind(), SEEDS, lambda: key, notify=lambda line: print("generated credential —", line, file=sys.stderr))


def downgrade() -> None:
    remove(op.get_bind(), SEEDS)
