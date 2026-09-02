"""create brokers

Revision ID: 002
Revises: 001
"""
import sqlalchemy as sa
from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "brokers",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("trading_platform_id", sa.Integer, sa.ForeignKey("trading_platforms.id"), nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )
    op.create_index("ix_brokers_trading_platform_id", "brokers", ["trading_platform_id"])


def downgrade() -> None:
    op.drop_index("ix_brokers_trading_platform_id", table_name="brokers")
    op.drop_table("brokers")
