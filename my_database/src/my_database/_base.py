"""Storage Adapter: Engine connection and session management."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from my_database._config import (
    InstanceConfig,
    RuntimeConfig,
    load_runtime_config,
    sqlite_database_path,
)


class Base(DeclarativeBase):
    """Shared declarative base for every persistence mapping in this package."""


_engines: dict[str, Engine] = {}
_session_factories: dict[str, sessionmaker[Session]] = {}
_runtime_config: RuntimeConfig | None = None


def get_runtime_config() -> RuntimeConfig:
    global _runtime_config
    if _runtime_config is None:
        _runtime_config = load_runtime_config()
    return _runtime_config


def _build_engine(instance: InstanceConfig) -> Engine:
    if instance.engine != "sqlite":
        raise ValueError(
            f"Unsupported Engine {instance.engine!r} for Instance {instance.key!r}."
        )
    path = sqlite_database_path(instance)
    engine = create_engine(
        f"sqlite:///{path}", connect_args={"check_same_thread": False}
    )

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(
        dbapi_connection: object, _connection_record: object
    ) -> None:
        cursor = dbapi_connection.cursor()  # type: ignore[attr-defined]
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def get_engine(instance_key: str) -> Engine:
    if instance_key not in _engines:
        config = get_runtime_config().resolve(instance_key)
        _engines[instance_key] = _build_engine(config)
    return _engines[instance_key]


def get_session_factory(instance_key: str) -> sessionmaker[Session]:
    if instance_key not in _session_factories:
        _session_factories[instance_key] = sessionmaker(
            bind=get_engine(instance_key), expire_on_commit=False
        )
    return _session_factories[instance_key]


@contextmanager
def session_scope(
    instance: str | None, *, existing: Session | None = None
) -> Generator[Session]:
    """One Session for the resolved Instance. Reuses `existing` when given (transaction grouping)."""
    if existing is not None:
        yield existing
        return
    resolved = get_runtime_config().resolve(instance)
    factory = get_session_factory(resolved.key)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_all_tables(instance_key: str | None = None) -> None:
    """Create every mapped table directly (test/dev convenience; production uses Migrations)."""
    resolved = get_runtime_config().resolve(instance_key)
    Base.metadata.create_all(get_engine(resolved.key))


def reset_engine_cache() -> None:
    """Dispose cached engines/sessions and forget runtime config (test isolation only)."""
    global _runtime_config
    for engine in _engines.values():
        engine.dispose()
    _engines.clear()
    _session_factories.clear()
    _runtime_config = None
