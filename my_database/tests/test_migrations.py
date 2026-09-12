"""Storage-schema migrations: forward, reversal, and drift detection."""

import sqlite3

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

from my_database import _orm
from my_database._config import CODE_PATH, DATA_DIR

_ALEMBIC_CONFIG_PATH = CODE_PATH / "alembic.ini"


def _table_names() -> set[str]:
    db_path = DATA_DIR / "trading_assistant_general.db"
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        return {row[0] for row in cursor.fetchall()}
    finally:
        connection.close()


def test_forward_migration_creates_every_mapped_table() -> None:
    names = _table_names()
    for orm_type in _orm.__all__:
        if orm_type == "Base":
            continue
        table_name = getattr(_orm, orm_type).__tablename__
        assert table_name in names


def test_downgrade_removes_the_schema_and_upgrade_restores_it() -> None:
    alembic_config = Config(str(_ALEMBIC_CONFIG_PATH))
    command.downgrade(alembic_config, "-1")
    assert _table_names() == {"alembic_version"}

    command.upgrade(alembic_config, "head")
    names = _table_names()
    assert "users" in names
    assert "positions" in names


def test_no_schema_drift_immediately_after_migrating() -> None:
    db_path = DATA_DIR / "trading_assistant_general.db"
    engine = create_engine(f"sqlite:///{db_path}")
    try:
        with engine.connect() as connection:
            migration_context = MigrationContext.configure(connection)
            diff = compare_metadata(migration_context, _orm.Base.metadata)
        assert diff == []
    finally:
        engine.dispose()
