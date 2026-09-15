"""Startup drift detection: does the running storage structure match the recorded Migration?"""

from __future__ import annotations

from typing import Any

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext

from database.adapter import get_engine
from database.mapping import build_all_tables


def detect_drift(instance_key: str | None = None) -> list[Any]:
    """Return the differences between the running structure and the recorded Migration history.

    An empty list means the running structure matches what the Migration history
    records; a non-empty list names each detected difference.
    """
    engine = get_engine(instance_key)
    metadata = build_all_tables()
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        return compare_metadata(context, metadata)


def is_up_to_date(instance_key: str | None = None) -> bool:
    """Whether the running structure has no detected drift from the recorded Migration history."""
    return len(detect_drift(instance_key)) == 0
