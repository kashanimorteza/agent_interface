"""Initial schema: the storage structure for every Domain Definition mapped in this phase.

Revision ID: 0001
Revises:
Create Date: 2026-09-14
"""

from __future__ import annotations

from alembic import op

from database.mapping import Base

revision: str = "0001"
down_revision: str | None = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
