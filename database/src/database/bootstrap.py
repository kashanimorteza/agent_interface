"""Bootstrap: applies pending Migrations, then verifies schema integrity.

Called before any normal data operation. Application code never issues raw
CREATE/ALTER/DROP; storage structure changes only through the recorded
Migration history (see ``migrations/``).
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import Engine

from database.config import PACKAGE_ROOT, load_storage_config, sqlite_url
from database.integrity import verify
from database.mapping import METADATA

_ALEMBIC_INI = PACKAGE_ROOT / "alembic.ini"

_ready_instances: set[str] = set()


def _alembic_config(instance: str) -> Config:
    cfg = Config(str(_ALEMBIC_INI))
    cfg.set_main_option("script_location", str(PACKAGE_ROOT / "migrations"))
    cfg.cmd_opts = SimpleNamespace(x=[f"instance={instance}"])  # type: ignore[attr-defined]
    return cfg


def ensure_ready(instance: str | None = None) -> Engine:
    """Apply pending Migrations and verify schema integrity for one Instance.

    Idempotent per process: repeated calls for the same already-verified
    Instance return immediately without re-running Migrations.
    """
    storage = load_storage_config()
    resolved = storage.resolve(instance).key

    from sqlalchemy import create_engine

    url = sqlite_url(resolved, config=storage)
    engine = create_engine(url)

    if resolved not in _ready_instances:
        alembic_cfg = _alembic_config(resolved)
        command.upgrade(alembic_cfg, "head")
        verify(engine, METADATA)
        _ready_instances.add(resolved)

    return engine


def reset_readiness_cache() -> None:
    """Test-only: forces the next ``ensure_ready`` call to re-verify integrity."""
    _ready_instances.clear()


def data_directory() -> Path:
    return PACKAGE_ROOT / "data"
