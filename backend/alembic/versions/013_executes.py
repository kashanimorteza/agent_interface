"""create executes

Revision ID: 013
Revises: 012
"""
import sqlalchemy as sa
from alembic import op

revision = "013"
down_revision = "012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "executes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("action_id", sa.Integer, sa.ForeignKey("actions.id"), nullable=False),
        sa.Column("profit", sa.Float, nullable=False),
        sa.Column("state", sa.String, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )
    op.create_index("ix_executes_action_id", "executes", ["action_id"])


def downgrade() -> None:
    op.drop_index("ix_executes_action_id", table_name="executes")
    op.drop_table("executes")
