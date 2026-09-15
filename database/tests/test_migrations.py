"""Verifies P2T4: ordered Migrations create the structure, reverse cleanly, and detect drift."""

from __future__ import annotations

import sqlite3

from alembic import command
from conftest import DB_FILE, alembic_config

from database.mapping import ALL_MODELS, table_name_for
from database.schema_check import is_up_to_date


def _table_names() -> set[str]:
    conn = sqlite3.connect(DB_FILE)
    try:
        rows = conn.execute(
            "select name from sqlite_master where type='table'"
        ).fetchall()
    finally:
        conn.close()
    return {row[0] for row in rows}


def test_upgrade_creates_every_persistent_models_table(fresh_db: None) -> None:
    expected = {table_name_for(m) for m in ALL_MODELS}
    assert expected.issubset(_table_names())


def test_downgrade_reverses_the_migration_cleanly(fresh_db: None) -> None:
    command.downgrade(alembic_config(), "base")
    remaining = _table_names() - {"alembic_version"}
    assert remaining == set()
    # leave a clean, migrated state so conftest teardown doesn't need it
    command.upgrade(alembic_config(), "head")


def test_no_drift_immediately_after_a_clean_migration(fresh_db: None) -> None:
    assert is_up_to_date() is True


def test_drift_is_detected_after_an_out_of_band_structural_change(
    fresh_db: None,
) -> None:
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("drop table positions")
        conn.commit()
    finally:
        conn.close()
    assert is_up_to_date() is False
