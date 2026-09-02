"""create strategies

Revision ID: 004
Revises: 003
"""
import sqlalchemy as sa
from alembic import op

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "strategies",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("risk_parameter", sa.Float, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("strategies")
