"""Storage Adapter: owns the connection to the selected Engine for every
configured Instance, and builds one SQLAlchemy Engine and session factory
per Instance on demand.
"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from my_database._config import DATA_DIR, load_runtime_configuration
from my_database._errors import UnknownInstanceError

_engines: dict[str, Engine] = {}
_session_factories: dict[str, sessionmaker[Session]] = {}


def _sqlite_url(database_name: str) -> str:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{DATA_DIR / f'{database_name}.db'}"


def _build_engine(instance_config: dict[str, object], engines_config: dict[str, dict]) -> Engine:
    engine_key = str(instance_config["engine"])
    engine_config = engines_config[engine_key]
    url = _sqlite_url(str(instance_config["database"]))
    engine = create_engine(
        url, connect_args={"check_same_thread": engine_config.get("check_same_thread", False)}
    )

    if engine_config.get("foreign_keys", True):

        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def _resolve_instance_key(instance: str | None) -> str:
    config = load_runtime_configuration()
    instances = config["instances"]
    default_instance = config["default_instance"]
    key = instance if instance is not None else default_instance
    if key not in instances:
        raise UnknownInstanceError(f"{key!r} is not a configured Database Instance.")
    return key


def get_session_factory(instance: str | None = None) -> sessionmaker[Session]:
    key = _resolve_instance_key(instance)
    if key not in _session_factories:
        config = load_runtime_configuration()
        engine = _build_engine(config["instances"][key], config["engines"])
        _engines[key] = engine
        _session_factories[key] = sessionmaker(bind=engine, expire_on_commit=False)
    return _session_factories[key]


def get_engine(instance: str | None = None) -> Engine:
    get_session_factory(instance)
    return _engines[_resolve_instance_key(instance)]
