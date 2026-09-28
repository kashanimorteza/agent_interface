"""Insert the initial Account data.

Revision ID: 0012
Revises: 0011
"""

import secrets
from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op

revision: str = "0012"
down_revision: str | Sequence[str] | None = "0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLE = "account"
_KEY = "name"
_KEYS = ["Acc-1"]


def _first(bind: sa.Connection, table: str) -> int:
    return bind.execute(sa.text(f'select min(id) from "{table}"')).scalar_one()


def upgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    op.bulk_insert(
        table,
        [
            {
                "name": "Acc-1",
                "username": "test",
                "password": secrets.token_urlsafe(32),
                "leverage": 100,
                "account_type": "CFD",
                "balance": Decimal(0),
                "is_active": True,
                "group_id": _first(bind, "accountgroup"),
                "broker_id": _first(bind, "broker"),
                "instance_id": _first(bind, "instance"),
                "base_currency_id": _first(bind, "currency"),
            }
        ],
    )


def downgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    bind.execute(sa.delete(table).where(table.c[_KEY].in_(_KEYS)))
