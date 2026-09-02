"""create trading_platforms

Revision ID: 001
Revises: 
"""
import sqlalchemy as sa
from alembic import op

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trading_platforms",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("trading_platforms")
