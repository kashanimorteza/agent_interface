from __future__ import annotations

from pathlib import Path

import sqlalchemy as sa
import yaml

_CODE_ROOT = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _CODE_ROOT / "database.yaml"


def _load_config() -> dict:
    with _CONFIG_PATH.open() as f:
        return yaml.safe_load(f)


CONFIG = _load_config()
_ENGINES: dict[str, sa.Engine] = {}


def instance_config(instance_key: str | None) -> dict:
    key = instance_key or CONFIG["default_instance"]
    instances = CONFIG["instances"]
    if key not in instances:
        raise ValueError(f"Unknown Database Instance: {key!r}")
    return {"key": key, **instances[key]}


def engine_for(instance_key: str | None = None) -> sa.Engine:
    cfg = instance_config(instance_key)
    key = cfg["key"]
    if key in _ENGINES:
        return _ENGINES[key]

    storage_path = _CODE_ROOT / cfg["storage_path"]
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    engine = sa.create_engine(
        f"sqlite:///{storage_path}",
        connect_args={"check_same_thread": False},
        poolclass=sa.pool.NullPool,
    )

    @sa.event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    _ENGINES[key] = engine
    return engine
