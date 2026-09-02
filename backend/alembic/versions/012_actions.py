"""create actions

Revision ID: 012
Revises: 011
"""
import sqlalchemy as sa
from alembic import op

revision = "012"
down_revision = "011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "actions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("asset_id", sa.Integer, sa.ForeignKey("assets.id"), nullable=False),
        sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.id"), nullable=False),
        sa.Column("strategy_id", sa.Integer, sa.ForeignKey("strategies.id"), nullable=False),
        sa.Column("group_id", sa.Integer, sa.ForeignKey("action_groups.id"), nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )
    op.create_index("ix_actions_asset_id", "actions", ["asset_id"])
    op.create_index("ix_actions_account_id", "actions", ["account_id"])
    op.create_index("ix_actions_strategy_id", "actions", ["strategy_id"])
    op.create_index("ix_actions_group_id", "actions", ["group_id"])


def downgrade() -> None:
    op.drop_index("ix_actions_asset_id", table_name="actions")
    op.drop_index("ix_actions_account_id", table_name="actions")
    op.drop_index("ix_actions_strategy_id", table_name="actions")
    op.drop_index("ix_actions_group_id", table_name="actions")
    op.drop_table("actions")
