"""Insert the initial Instance data.

Revision ID: 0010
Revises: 0009
"""

import secrets
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010"
down_revision: str | Sequence[str] | None = "0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLE = "instance"
_KEY = "name"
_KEYS = ["MetaTrader"]


def _first(bind: sa.Connection, table: str) -> int:
    return bind.execute(sa.text(f'select min(id) from "{table}"')).scalar_one()


def upgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    op.bulk_insert(
        table,
        [
            {
                "name": "MetaTrader",
                "ip": "127.0.0.1",
                "username": "test",
                "password": secrets.token_urlsafe(32),
                "api_key": secrets.token_urlsafe(32),
                "is_active": True,
                "user_id": _first(bind, "user"),
                "trading_platform_id": _first(bind, "tradingplatform"),
            }
        ],
    )


def downgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    bind.execute(sa.delete(table).where(table.c[_KEY].in_(_KEYS)))
