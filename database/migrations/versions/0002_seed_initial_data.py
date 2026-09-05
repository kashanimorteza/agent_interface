"""seed_initial_data

Revision ID: 0002
Revises: 0001

Applies the project's declared initial records idempotently and reports each
generated secret once on stderr; downgrade removes the seeded records.
"""
from typing import Sequence, Union
import sys

from alembic import op
from sqlalchemy.orm import Session

from ta_database.data_logic.initial_data.apply import apply_seed, remove_seed

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with Session(bind=op.get_bind()) as session:
        result = apply_seed(session)
        session.commit()
    for (model_key, key_values, field), plain in result["generated"].items():
        print(f"[seed] generated {model_key} {key_values} {field}: {plain}", file=sys.stderr)


def downgrade() -> None:
    with Session(bind=op.get_bind()) as session:
        remove_seed(session)
        session.commit()
