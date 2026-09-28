"""Insert the initial Asset data.

Revision ID: 0011
Revises: 0010
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011"
down_revision: str | Sequence[str] | None = "0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLE = "asset"
_KEY = "symbol"
_KEYS = ["EUR/USD", "EUR/GBP", "XAU/USD", "USOil"]


def _first(bind: sa.Connection, table: str) -> int:
    return bind.execute(sa.text(f'select min(id) from "{table}"')).scalar_one()


def upgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    op.bulk_insert(
        table,
        [
            {
                "symbol": "EUR/USD",
                "category": "Currency",
                "point_size": 0.0001,
                "digits": 5,
                "is_active": True,
                "broker_id": _first(bind, "broker"),
            },
            {
                "symbol": "EUR/GBP",
                "category": "Currency",
                "point_size": 0.001,
                "digits": 5,
                "is_active": True,
                "broker_id": _first(bind, "broker"),
            },
            {
                "symbol": "XAU/USD",
                "category": "Commodity",
                "point_size": 0.01,
                "digits": 2,
                "is_active": True,
                "broker_id": _first(bind, "broker"),
            },
            {
                "symbol": "USOil",
                "category": "Commodity",
                "point_size": 0.01,
                "digits": 3,
                "is_active": True,
                "broker_id": _first(bind, "broker"),
            },
        ],
    )


def downgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    bind.execute(sa.delete(table).where(table.c[_KEY].in_(_KEYS)))
