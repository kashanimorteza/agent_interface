"""Storage Adapter: owns the connection to the selected Engine per Instance."""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from ._config import DatabaseConfig, InstanceDefinition, load_config

_config: DatabaseConfig = load_config()
_engines: dict[str, Engine] = {}
_session_factories: dict[str, sessionmaker[Session]] = {}


def get_config() -> DatabaseConfig:
    return _config


def _build_engine(instance: InstanceDefinition) -> Engine:
    url = _config.sqlalchemy_url(instance)
    engine = create_engine(url, future=True)

    engine_profile = _config.engines[instance.engine_key]
    if engine_profile.foreign_keys:

        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _record) -> None:  # noqa: ANN001
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def engine_for(instance_key: str | None = None) -> Engine:
    instance = _config.resolve(instance_key)
    if instance.key not in _engines:
        _engines[instance.key] = _build_engine(instance)
    return _engines[instance.key]


def session_for(instance_key: str | None = None) -> Session:
    instance = _config.resolve(instance_key)
    if instance.key not in _session_factories:
        _session_factories[instance.key] = sessionmaker(
            bind=engine_for(instance.key), expire_on_commit=False
        )
    return _session_factories[instance.key]()
