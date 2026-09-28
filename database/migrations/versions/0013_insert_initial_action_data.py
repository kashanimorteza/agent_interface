"""Insert the initial Action data.

Revision ID: 0013
Revises: 0012
"""

from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op

revision: str = "0013"
down_revision: str | Sequence[str] | None = "0012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLE = "action"
_KEY = "name"
_KEYS = ["Default"]


def _first(bind: sa.Connection, table: str) -> int:
    return bind.execute(sa.text(f'select min(id) from "{table}"')).scalar_one()


def upgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    op.bulk_insert(
        table,
        [
            {
                "name": "Default",
                "risk_by_reward": Decimal(1),
                "take_profit": Decimal(1),
                "stop_loss": Decimal(1),
                "is_active": True,
                "action_group_id": _first(bind, "actiongroup"),
                "asset_id": _first(bind, "asset"),
                "account_id": _first(bind, "account"),
                "partial_group_id": _first(bind, "partialgroup"),
                "trailing_group_id": _first(bind, "trailinggroup"),
            }
        ],
    )


def downgrade() -> None:
    bind = op.get_bind()
    table = sa.Table(_TABLE, sa.MetaData(), autoload_with=bind)
    bind.execute(sa.delete(table).where(table.c[_KEY].in_(_KEYS)))
