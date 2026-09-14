from pathlib import Path
from typing import Any, NamedTuple

import yaml
from sqlalchemy import Engine, create_engine, event

_COMPONENT_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = _COMPONENT_ROOT / "database.yaml"

with _CONFIG_PATH.open() as _f:
    _CONFIG: dict[str, Any] = yaml.safe_load(_f)

_engines: dict[str, Engine] = {}


class InstanceInfo(NamedTuple):
    key: str
    name: str
    purpose: str


def list_instances() -> list[InstanceInfo]:
    return [
        InstanceInfo(key=key, name=cfg["name"], purpose=cfg["purpose"])
        for key, cfg in _CONFIG["instances"].items()
    ]


def default_instance() -> str:
    return str(_CONFIG["default_instance"])


def _instance_config(key: str) -> dict[str, Any]:
    try:
        config: dict[str, Any] = _CONFIG["instances"][key]
        return config
    except KeyError:
        raise ValueError(f"Unknown Database Instance: {key!r}") from None


def _configure_sqlite(engine: Engine) -> None:
    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection: Any, connection_record: Any) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_engine(instance: str | None = None) -> Engine:
    key = instance or default_instance()
    cfg = _instance_config(key)
    if key not in _engines:
        engine_name = cfg["engine"]
        if engine_name == "sqlite":
            data_dir = _COMPONENT_ROOT / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = data_dir / f"{cfg['database']}.db"
            engine = create_engine(f"sqlite:///{db_path}", future=True)
            _configure_sqlite(engine)
        else:
            raise ValueError(f"Unsupported Engine: {engine_name!r}")
        _engines[key] = engine
    return _engines[key]
