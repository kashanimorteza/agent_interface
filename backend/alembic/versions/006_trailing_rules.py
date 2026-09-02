"""create trailing_rules

Revision ID: 006
Revises: 005
"""
import sqlalchemy as sa
from alembic import op

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trailing_rules",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("trailing_group_id", sa.Integer, sa.ForeignKey("trailing_groups.id"), nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )
    op.create_index("ix_trailing_rules_trailing_group_id", "trailing_rules", ["trailing_group_id"])


def downgrade() -> None:
    op.drop_index("ix_trailing_rules_trailing_group_id", table_name="trailing_rules")
    op.drop_table("trailing_rules")
