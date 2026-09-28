"""Insert the initial Currency data.

Revision ID: 0005
Revises: 0004
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005"
down_revision: str | Sequence[str] | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLE = "currency"
_KEY = "code"
_KEYS = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"]


def _first(bind: sa.Connection, table: str) -> int:
    return bind.execute(sa.text(f'select min(id) from "{table}"')).scalar_one()


def upgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    op.bulk_insert(
        table,
        [
            {
                "code": "USD",
                "symbol": "$",
                "country": "United States",
                "decimal_digits": 2,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
            {
                "code": "EUR",
                "symbol": "€",
                "country": "Eurozone",
                "decimal_digits": 2,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
            {
                "code": "GBP",
                "symbol": "£",
                "country": "United Kingdom",
                "decimal_digits": 2,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
            {
                "code": "JPY",
                "symbol": "¥",
                "country": "Japan",
                "decimal_digits": 0,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
            {
                "code": "CHF",
                "symbol": "CHF",
                "country": "Switzerland",
                "decimal_digits": 2,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
            {
                "code": "CAD",
                "symbol": "C$",
                "country": "Canada",
                "decimal_digits": 2,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
            {
                "code": "AUD",
                "symbol": "A$",
                "country": "Australia",
                "decimal_digits": 2,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
            {
                "code": "NZD",
                "symbol": "NZ$",
                "country": "New Zealand",
                "decimal_digits": 2,
                "is_active": True,
                "user_id": _first(bind, "user"),
            },
        ],
    )


def downgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    bind.execute(sa.delete(table).where(table.c[_KEY].in_(_KEYS)))
