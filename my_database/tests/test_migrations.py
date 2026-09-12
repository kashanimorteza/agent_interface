"""The recorded migration history reproduces the complete schema from nothing, and reverses cleanly."""

from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def _run_alembic(*args: str) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=_PACKAGE_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def _table_names(db_path: Path) -> set[str]:
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return {row[0] for row in cursor.fetchall()}
    finally:
        conn.close()


def test_migration_history_creates_and_reverses_the_complete_schema():
    db_path = _PACKAGE_ROOT / "data" / "general.db"
    # Start from genuinely nothing: the autouse fixture creates tables directly
    # (not through Alembic), so remove that file before Alembic sees it.
    if db_path.exists():
        db_path.unlink()

    _run_alembic("upgrade", "head")
    tables = _table_names(db_path)
    expected = {
        "users",
        "trading_platforms",
        "currencies",
        "brokers",
        "instances",
        "assets",
        "account_groups",
        "accounts",
        "trailing_groups",
        "trailing_rules",
        "partial_groups",
        "partial_rules",
        "action_groups",
        "actions",
        "positions",
        "alembic_version",
    }
    assert expected <= tables

    _run_alembic("downgrade", "base")
    # alembic_version is Alembic's own bookkeeping table and is expected to
    # remain (empty) after downgrading to base; only our mapped tables must be gone.
    assert _table_names(db_path) <= {"alembic_version"}
