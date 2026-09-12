"""Migration history: reproduces the exact schema and reverses cleanly (Task P2-T3)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "migrations"))
import _integrity  # noqa: E402

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def test_upgrade_creates_exactly_the_resolved_schema():
    from my_database._orm import Base

    insp = inspect(
        create_engine(f"sqlite:///{_PACKAGE_ROOT / 'data' / 'trading_assistant_general.db'}")
    )
    live_tables = set(insp.get_table_names()) - {"alembic_version"}
    expected_tables = set(Base.metadata.tables.keys())
    assert live_tables == expected_tables


def test_downgrade_then_upgrade_reproduces_schema(tmp_path):
    isolated_ini = tmp_path / "alembic.ini"
    isolated_ini.write_text((_PACKAGE_ROOT / "alembic.ini").read_text())
    cfg = Config(str(isolated_ini))
    cfg.set_main_option("script_location", str(_PACKAGE_ROOT / "migrations"))

    import my_database._config as config_module

    original_data_dir = config_module._DATA_DIR
    config_module._DATA_DIR = tmp_path / "data"
    try:
        command.upgrade(cfg, "head")
        db_path = tmp_path / "data" / "trading_assistant_general.db"
        assert db_path.exists()

        insp = inspect(create_engine(f"sqlite:///{db_path}"))
        assert set(insp.get_table_names()) - {"alembic_version"}

        command.downgrade(cfg, "base")
        insp = inspect(create_engine(f"sqlite:///{db_path}"))
        assert set(insp.get_table_names()) - {"alembic_version"} == set()
    finally:
        config_module._DATA_DIR = original_data_dir
        shutil.rmtree(tmp_path / "data", ignore_errors=True)


def test_migration_integrity_manifest_matches_current_files():
    assert _integrity.verify_manifest() == []


def test_no_schema_drift_against_the_live_migrated_database():
    from my_database._schema_check import detect_drift

    engine = create_engine(f"sqlite:///{_PACKAGE_ROOT / 'data' / 'trading_assistant_general.db'}")
    assert detect_drift(engine) == []
