"""Storage Adapter: owns the connection to the selected Engine for each Instance.

No other layer in this package opens a connection directly; every physical
persistence operation goes through an Engine resolved here.
"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, event

from . import _config

_ENGINES: dict[str, Engine] = {}


def _create_sqlite_engine(instance: _config.InstanceConfig) -> Engine:
    path = _config.sqlite_storage_path(instance)
    path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{path}", future=True)

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def resolve_instance_key(instance: str | None) -> str:
    if instance is None:
        return _config.default_instance_key()
    instances = _config.load_instances()
    if instance not in instances:
        raise UnknownInstanceError(f"Instance {instance!r} is not configured.")
    return instance


def engine_for(instance: str | None = None) -> Engine:
    """The managed Engine for a configured Instance, resolving the default when omitted."""
    key = resolve_instance_key(instance)
    if key not in _ENGINES:
        instances = _config.load_instances()
        cfg = instances[key]
        if cfg.engine == "SQLite":
            _ENGINES[key] = _create_sqlite_engine(cfg)
        else:
            raise UnsupportedEngineError(f"Engine {cfg.engine!r} has no Storage Adapter implementation.")
    return _ENGINES[key]


class UnknownInstanceError(ValueError):
    pass


class UnsupportedEngineError(ValueError):
    pass
