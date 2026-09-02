"""create accounts

Revision ID: 011
Revises: 010
"""
import sqlalchemy as sa
from alembic import op

revision = "011"
down_revision = "010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("broker_id", sa.Integer, sa.ForeignKey("brokers.id"), nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )
    op.create_index("ix_accounts_broker_id", "accounts", ["broker_id"])


def downgrade() -> None:
    op.drop_index("ix_accounts_broker_id", table_name="accounts")
    op.drop_table("accounts")
