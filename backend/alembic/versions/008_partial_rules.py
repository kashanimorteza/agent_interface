"""create partial_rules

Revision ID: 008
Revises: 007
"""
import sqlalchemy as sa
from alembic import op

revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "partial_rules",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("partial_group_id", sa.Integer, sa.ForeignKey("partial_groups.id"), nullable=False),
        sa.Column("profit_threshold", sa.Float, nullable=False),
        sa.Column("close_portion", sa.Float, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )
    op.create_index("ix_partial_rules_partial_group_id", "partial_rules", ["partial_group_id"])


def downgrade() -> None:
    op.drop_index("ix_partial_rules_partial_group_id", table_name="partial_rules")
    op.drop_table("partial_rules")
