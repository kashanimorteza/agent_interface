"""Initial data: seed the resolved initial records (database.yaml data_logic.initial_data).

CREDENTIAL_ENCRYPTION_KEY must be set when upgrading because the seeded account password is encrypted.
Generated credentials (admin password, admin API key, account password) are printed exactly once
during the upgrade as GENERATED CREDENTIAL lines and are never stored in plain form.

Revision ID: 0002_initial_data
Revises: 0001_storage_schema
"""
from typing import Sequence, Union

from alembic import op

from my_database.storage_adapter.seed import seed, unseed

# revision identifiers, used by Alembic.
revision: str = "0002_initial_data"
down_revision: Union[str, Sequence[str], None] = "0001_storage_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert the initial records that are not present yet (matched by natural key)."""
    seed(op.get_bind())


def downgrade() -> None:
    """Remove the initial records (matched by natural key); tables remain."""
    unseed(op.get_bind())
