"""Insert the initial Broker data.

Revision ID: 0004
Revises: 0003
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: str | Sequence[str] | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLE = "broker"
_KEY = "name"
_KEYS = ["FxPro"]


def _first(bind: sa.Connection, table: str) -> int:
    return bind.execute(sa.text(f'select min(id) from "{table}"')).scalar_one()


def upgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    op.bulk_insert(
        table,
        [
            {
                "name": "FxPro",
                "is_active": True,
                "user_id": _first(bind, "user"),
            }
        ],
    )


def downgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    bind.execute(sa.delete(table).where(table.c[_KEY].in_(_KEYS)))
