"""Configuration (Core): loading and validating the Database Configuration."""

import functools
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from model import entities

from database.core.errors import (
    ConfigurationError,
    InactiveInstanceError,
    InvalidInputError,
)
from database.core.values import Connection, FilterCombination, OrderDirection

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
CONFIGURATION_FILE = COMPONENT_ROOT / "config.yaml"

_TOP_LEVEL = {"engines", "instances", "settings", "initial_data"}
_ENGINE_KEYS = {"name", "driver", "parameters"}
_INSTANCE_KEYS = {
    "name",
    "active",
    "engine",
    "host",
    "port",
    "database",
    "username",
    "password",
    "options",
}
_SETTINGS_KEYS = {"default_instance", "storage_root", "query", "setup"}
_QUERY_KEYS = {"filter_combination", "default_limit", "default_order"}
_ORDER_KEYS = {"field", "direction"}
_AFTER_GENERATION_KEYS = {"enabled", "fail_on_error", "command"}


@dataclass(frozen=True)
class EngineConfig:
    key: str
    name: str
    driver: str
    parameters: dict[str, Any]


@dataclass(frozen=True)
class InstanceConfig:
    key: str
    name: str
    active: bool
    engine: str
    host: str | None
    port: int | None
    database: str
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: dict[str, Any] = field(repr=False)


@dataclass(frozen=True)
class QueryDefaults:
    filter_combination: FilterCombination
    default_limit: int
    order_field: str
    order_direction: OrderDirection


@dataclass(frozen=True)
class InitialDataSet:
    entity: str
    records: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class Configuration:
    engines: dict[str, EngineConfig]
    instances: dict[str, InstanceConfig]
    default_instance: str
    storage_root: Path
    query: QueryDefaults
    after_generation_enabled: bool
    after_generation_fail_on_error: bool
    initial_data: tuple[InitialDataSet, ...]


def _mapping(value: Any, label: str, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"{label} must be a mapping")
    if set(value) != keys:
        raise ConfigurationError(f"{label} must have exactly the keys {sorted(keys)}")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ConfigurationError(f"{label} must be a non-empty string")
    return value


def _flag(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ConfigurationError(f"{label} must be a boolean")
    return value


def _member[E: Enum](enumeration: type[E], value: Any, label: str) -> E:
    try:
        return enumeration[value]
    except KeyError, TypeError:
        names = ", ".join(member.name for member in enumeration)
        raise ConfigurationError(f"{label} must be one of {names}") from None


def _engines(raw: Any) -> dict[str, EngineConfig]:
    if not isinstance(raw, dict) or not raw:
        raise ConfigurationError("engines must be a non-empty mapping")
    result = {}
    for key, value in raw.items():
        body = _mapping(value, f"Engine {key!r}", _ENGINE_KEYS)
        if not isinstance(body["parameters"], dict):
            raise ConfigurationError(f"Engine {key!r}: parameters must be a mapping")
        result[_text(key, "An Engine key")] = EngineConfig(
            key=key,
            name=_text(body["name"], f"Engine {key!r} name"),
            driver=_text(body["driver"], f"Engine {key!r} driver"),
            parameters=body["parameters"],
        )
    return result


def _instances(raw: Any, engines: dict[str, EngineConfig]) -> dict[str, InstanceConfig]:
    if not isinstance(raw, dict) or not raw:
        raise ConfigurationError("instances must be a non-empty mapping")
    result = {}
    members: set[str] = set()
    names: set[str] = set()
    for key, value in raw.items():
        label = f"Instance {key!r}"
        body = _mapping(value, label, _INSTANCE_KEYS)
        member = _text(key, "An Instance key").upper()
        if not member.isidentifier() or member in members:
            raise ConfigurationError(f"{label} has no unique public member name")
        members.add(member)
        name = _text(body["name"], f"{label} name")
        if name in names:
            raise ConfigurationError(f"{label} repeats an Instance name")
        names.add(name)
        if body["engine"] not in engines:
            raise ConfigurationError(f"{label} names an undeclared Engine")
        port = body["port"]
        if port is not None and (isinstance(port, bool) or not isinstance(port, int)):
            raise ConfigurationError(f"{label}: port must be an integer or null")
        for part in ("host", "username", "password"):
            if body[part] is not None and not isinstance(body[part], str):
                raise ConfigurationError(f"{label}: {part} must be a string or null")
        if not isinstance(body["options"], dict):
            raise ConfigurationError(f"{label}: options must be a mapping")
        result[key] = InstanceConfig(
            key=key,
            name=name,
            active=_flag(body["active"], f"{label} active"),
            engine=body["engine"],
            host=body["host"],
            port=port,
            database=_text(body["database"], f"{label} database"),
            username=body["username"],
            password=body["password"],
            options=body["options"],
        )
    return result


def _check_required_values(instance: InstanceConfig, engine: EngineConfig) -> None:
    connection = engine.parameters.get("connection", {})
    for part in connection.get("required_parameters", []):
        if getattr(instance, part, None) in (None, ""):
            raise ConfigurationError(
                f"Instance {instance.key!r} lacks the required value {part!r}"
            )


def _storage_root(raw: Any) -> Path:
    text = _text(raw, "settings.storage_root")
    path = Path(text)
    root = (COMPONENT_ROOT / path).resolve()
    if (
        path.is_absolute()
        or not root.is_relative_to(COMPONENT_ROOT)
        or root == COMPONENT_ROOT
    ):
        raise ConfigurationError(
            "settings.storage_root must be a directory inside the Database Component"
        )
    return root


def _storage_path(storage_root: Path, instance: InstanceConfig) -> Path:
    path = Path(instance.database)
    resolved = (storage_root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(storage_root):
        raise ConfigurationError(
            f"Instance {instance.key!r} has a storage path outside the Database storage"
        )
    return resolved


def _is_file_backed(engine: EngineConfig) -> bool:
    return engine.parameters.get("storage", {}).get("kind") == "file"


def _initial_data(raw: Any) -> tuple[InitialDataSet, ...]:
    if not isinstance(raw, list):
        raise ConfigurationError("initial_data must be a list")
    known = {entity.__name__ for entity in entities}
    seen: set[str] = set()
    result = []
    for item in raw:
        body = _mapping(item, "An initial_data entry", {"entity", "records"})
        name = body["entity"]
        if name not in known or name in seen:
            raise ConfigurationError(
                f"initial_data names an unknown or repeated Entity {name!r}"
            )
        seen.add(name)
        records = body["records"]
        if not isinstance(records, list) or not all(
            isinstance(record, dict) for record in records
        ):
            raise ConfigurationError(f"initial_data records of {name} must be mappings")
        result.append(InitialDataSet(entity=name, records=tuple(records)))
    return tuple(result)


def parse(raw: Any) -> Configuration:
    """Validate a decoded Configuration and return it."""
    top = _mapping(raw, "The Database Configuration", _TOP_LEVEL)
    engines = _engines(top["engines"])
    instances = _instances(top["instances"], engines)
    settings = _mapping(top["settings"], "settings", _SETTINGS_KEYS)
    default = settings["default_instance"]
    if default not in instances or not instances[default].active:
        raise ConfigurationError(
            "settings.default_instance must name an active Instance"
        )
    storage_root = _storage_root(settings["storage_root"])
    query = _mapping(settings["query"], "settings.query", _QUERY_KEYS)
    order = _mapping(
        query["default_order"], "settings.query.default_order", _ORDER_KEYS
    )
    limit = query["default_limit"]
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ConfigurationError("settings.query.default_limit must be an integer")
    setup = _mapping(settings["setup"], "settings.setup", {"after_generation"})
    after = _mapping(
        setup["after_generation"],
        "settings.setup.after_generation",
        _AFTER_GENERATION_KEYS,
    )
    if after["command"] != "prepare":
        raise ConfigurationError(
            "settings.setup.after_generation.command must be prepare"
        )
    for instance in instances.values():
        if instance.active:
            engine = engines[instance.engine]
            _check_required_values(instance, engine)
            if _is_file_backed(engine):
                _storage_path(storage_root, instance)
    return Configuration(
        engines=engines,
        instances=instances,
        default_instance=default,
        storage_root=storage_root,
        query=QueryDefaults(
            filter_combination=_member(
                FilterCombination,
                query["filter_combination"],
                "settings.query.filter_combination",
            ),
            default_limit=limit if limit > 0 else -1,
            order_field=_text(order["field"], "settings.query.default_order.field"),
            order_direction=_member(
                OrderDirection,
                order["direction"],
                "settings.query.default_order.direction",
            ),
        ),
        after_generation_enabled=_flag(after["enabled"], "after_generation.enabled"),
        after_generation_fail_on_error=_flag(
            after["fail_on_error"], "after_generation.fail_on_error"
        ),
        initial_data=_initial_data(top["initial_data"]),
    )


@functools.cache
def load() -> Configuration:
    """Load and validate the Database Configuration of the Component."""
    if "site-packages" in COMPONENT_ROOT.parts or not CONFIGURATION_FILE.is_file():
        raise ConfigurationError(
            "The Database Configuration was not found at the Component root"
        )
    try:
        raw = yaml.safe_load(CONFIGURATION_FILE.read_text(encoding="utf-8"))
    except OSError, yaml.YAMLError:
        raise ConfigurationError("The Database Configuration cannot be read") from None
    return parse(raw)


@functools.cache
def instance_enum() -> type[Enum]:
    """The DatabaseInstance enumeration: one member per active Instance."""
    members = {
        instance.key.upper(): instance.key
        for instance in load().instances.values()
        if instance.active
    }
    return Enum("database_instance", members)


def select_instance(instance: Any) -> InstanceConfig:
    """Return the Instance a call runs on; no member selects the default."""
    configuration = load()
    if instance is None:
        return configuration.instances[configuration.default_instance]
    if not isinstance(instance, instance_enum()):
        raise InvalidInputError("The Instance must be a DatabaseInstance member")
    selected = configuration.instances[instance.value]
    if not selected.active:
        raise InactiveInstanceError(f"Instance {selected.key!r} is not active")
    return selected


def connection(instance: InstanceConfig) -> Connection:
    """Resolve the complete connection of an Instance from the Configuration."""
    configuration = load()
    engine = configuration.engines[instance.engine]
    return Connection(
        instance=instance.key,
        engine=instance.engine,
        host=instance.host,
        port=instance.port,
        database=instance.database,
        username=instance.username,
        password=instance.password,
        options=instance.options,
        parameters=engine.parameters,
        storage_path=(
            _storage_path(configuration.storage_root, instance)
            if _is_file_backed(engine)
            else None
        ),
    )
