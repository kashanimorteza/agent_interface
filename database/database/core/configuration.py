"""Loading and validation of the Database Configuration: the sole runtime source of Engines, Instances,
settings and Initial Data."""

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from database.core.errors import (
    ConfigurationError,
    InactiveInstanceError,
    InvalidInputError,
)
from database.core.values import Connection, FilterCombination, OrderDirection

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
CONFIGURATION_FILE = COMPONENT_ROOT / "config.yaml"

_KEY = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_CONNECTION_VALUES = ("host", "port", "database", "username", "password")


@dataclass(frozen=True, slots=True)
class EngineConfiguration:
    key: str
    name: str
    driver: str
    parameters: dict[str, Any] = field(repr=False)

    @property
    def storage_kind(self) -> str | None:
        storage = self.parameters.get("storage")
        return storage.get("kind") if isinstance(storage, dict) else None

    @property
    def required_parameters(self) -> tuple[str, ...]:
        connection = self.parameters.get("connection")
        required = (
            connection.get("required_parameters")
            if isinstance(connection, dict)
            else None
        )
        return tuple(required) if isinstance(required, list) else ()


@dataclass(frozen=True, slots=True)
class InstanceConfiguration:
    key: str
    name: str
    active: bool
    engine: str
    host: str | None = field(repr=False)
    port: int | None = field(repr=False)
    database: str = field(repr=False)
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: dict[str, Any] = field(repr=False)


@dataclass(frozen=True, slots=True)
class Settings:
    default_instance: str
    storage_root: Path
    filter_combination: FilterCombination
    default_limit: int
    default_order_field: str
    default_order_direction: OrderDirection
    after_generation_enabled: bool
    after_generation_fail_on_error: bool
    after_generation_command: str


@dataclass(frozen=True, slots=True)
class InitialData:
    entity: str
    records: tuple[dict[str, Any], ...]


@dataclass(frozen=True, slots=True)
class Configuration:
    engines: dict[str, EngineConfiguration]
    instances: dict[str, InstanceConfiguration]
    settings: Settings
    initial_data: tuple[InitialData, ...]


def _fail(message: str) -> ConfigurationError:
    return ConfigurationError(f"Invalid Database Configuration: {message}")


def _mapping(value: Any, keys: tuple[str, ...], where: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != set(keys):
        raise _fail(f"{where} must hold exactly {', '.join(keys)}.")
    return value


def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise _fail(f"{where} must be a non-empty string.")
    return value


def _flag(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        raise _fail(f"{where} must be a boolean.")
    return value


def _contained(root: Path, relative: str, where: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute():
        raise _fail(f"{where} must be relative.")
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(root.resolve()) or resolved == root.resolve():
        raise _fail(f"{where} escapes its storage.")
    return resolved


def _engines(raw: Any) -> dict[str, EngineConfiguration]:
    if not isinstance(raw, dict) or not raw:
        raise _fail("engines must be a non-empty mapping.")
    engines: dict[str, EngineConfiguration] = {}
    for key, item in raw.items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise _fail("an Engine key is not valid.")
        item = _mapping(item, ("name", "driver", "parameters"), f"Engine {key}")
        if not isinstance(item["parameters"], dict):
            raise _fail(f"Engine {key} parameters must be a mapping.")
        engines[key] = EngineConfiguration(
            key,
            _text(item["name"], f"Engine {key} name"),
            _text(item["driver"], f"Engine {key} driver"),
            item["parameters"],
        )
    return engines


def _instances(
    raw: Any, engines: dict[str, EngineConfiguration], storage: Path
) -> dict[str, InstanceConfiguration]:
    if not isinstance(raw, dict) or not raw:
        raise _fail("instances must be a non-empty mapping.")
    members = (
        "name",
        "active",
        "engine",
        "host",
        "port",
        "database",
        "username",
        "password",
        "options",
    )
    instances: dict[str, InstanceConfiguration] = {}
    for key, item in raw.items():
        if not isinstance(key, str) or not _KEY.fullmatch(key):
            raise _fail("an Instance key is not valid.")
        item = _mapping(item, members, f"Instance {key}")
        engine = item["engine"]
        if engine not in engines:
            raise _fail(f"Instance {key} names an Engine that is not declared.")
        for optional in ("host", "username", "password"):
            if item[optional] is not None and not isinstance(item[optional], str):
                raise _fail(f"Instance {key} {optional} must be text or null.")
        port = item["port"]
        if port is not None and (not isinstance(port, int) or isinstance(port, bool)):
            raise _fail(f"Instance {key} port must be an integer or null.")
        if not isinstance(item["options"], dict) or not isinstance(
            item["database"], str
        ):
            raise _fail(f"Instance {key} database and options are not valid.")
        active = _flag(item["active"], f"Instance {key} active")
        instance = InstanceConfiguration(
            key,
            _text(item["name"], f"Instance {key} name"),
            active,
            engine,
            item["host"],
            port,
            item["database"],
            item["username"],
            item["password"],
            item["options"],
        )
        if active:
            for required in engines[engine].required_parameters:
                if required not in _CONNECTION_VALUES or getattr(
                    instance, required
                ) in (None, ""):
                    raise _fail(f"Instance {key} lacks a value its Engine requires.")
            if engines[engine].storage_kind == "file":
                _contained(storage, instance.database, f"Instance {key} database")
        instances[key] = instance
    if len({key.upper() for key in instances}) != len(instances) or len(
        {i.name for i in instances.values()}
    ) != len(instances):
        raise _fail("Instance keys and names must be unique.")
    return instances


def _settings(raw: Any, instances: dict[str, InstanceConfiguration]) -> Settings:
    raw = _mapping(
        raw, ("default_instance", "storage_root", "query", "setup"), "settings"
    )
    default = raw["default_instance"]
    if default not in instances or not instances[default].active:
        raise _fail("the default Instance must be an active declared Instance.")
    query = _mapping(
        raw["query"],
        ("filter_combination", "default_limit", "default_order"),
        "settings.query",
    )
    order = _mapping(
        query["default_order"], ("field", "direction"), "settings.query.default_order"
    )
    setup = _mapping(raw["setup"], ("after_generation",), "settings.setup")
    after = _mapping(
        setup["after_generation"],
        ("enabled", "fail_on_error", "command"),
        "settings.setup.after_generation",
    )
    if query["filter_combination"] not in FilterCombination.__members__:
        raise _fail("the default Filter combination is not a known name.")
    if order["direction"] not in OrderDirection.__members__:
        raise _fail("the default Order direction is not a known name.")
    limit = query["default_limit"]
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise _fail("the default limit must be an integer.")
    if after["command"] != "prepare":
        raise _fail("the after-generation command must be prepare.")
    root = raw["storage_root"]
    _text(root, "settings.storage_root")
    return Settings(
        default,
        _contained(COMPONENT_ROOT, root, "settings.storage_root"),
        FilterCombination[query["filter_combination"]],
        limit if limit > 0 else -1,
        _text(order["field"], "settings.query.default_order.field"),
        OrderDirection[order["direction"]],
        _flag(after["enabled"], "after_generation.enabled"),
        _flag(after["fail_on_error"], "after_generation.fail_on_error"),
        after["command"],
    )


def _initial_data(raw: Any) -> tuple[InitialData, ...]:
    if not isinstance(raw, list):
        raise _fail("initial_data must be a list.")
    groups = []
    for item in raw:
        item = _mapping(item, ("entity", "records"), "an Initial Data group")
        records = item["records"]
        if not isinstance(records, list) or not all(
            isinstance(r, dict) and all(isinstance(k, str) for k in r) for r in records
        ):
            raise _fail("Initial Data records must be mappings of Field values.")
        groups.append(
            InitialData(_text(item["entity"], "an Initial Data entity"), tuple(records))
        )
    return tuple(groups)


def load_configuration(path: Path = CONFIGURATION_FILE) -> Configuration:
    """Load and validate the Database Configuration; any violation fails before a connection is opened."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError, yaml.YAMLError:
        raise _fail("the file could not be read.") from None
    raw = _mapping(
        raw, ("engines", "instances", "settings", "initial_data"), "the file"
    )
    engines = _engines(raw["engines"])
    settings_root = _contained(
        COMPONENT_ROOT,
        _text(
            raw["settings"].get("storage_root")
            if isinstance(raw["settings"], dict)
            else None,
            "settings.storage_root",
        ),
        "settings.storage_root",
    )
    instances = _instances(raw["instances"], engines, settings_root)
    return Configuration(
        engines,
        instances,
        _settings(raw["settings"], instances),
        _initial_data(raw["initial_data"]),
    )


CONFIGURATION = load_configuration()

database_instance = Enum(
    "database_instance",
    {
        key.upper(): key
        for key, instance in CONFIGURATION.instances.items()
        if instance.active
    },
    module=__name__,
)


def resolve_instance(selection: Any) -> InstanceConfiguration:
    """Resolve an optional DatabaseInstance member to its configured Instance, before any storage is touched."""
    if selection is None:
        key = CONFIGURATION.settings.default_instance
    elif isinstance(selection, database_instance):
        key = selection.value
    else:
        raise InvalidInputError(
            "An Instance is selected only by a member of the Instance group."
        )
    instance = CONFIGURATION.instances.get(key)
    if instance is None:
        raise ConfigurationError("The selected Instance is not configured.")
    if not instance.active:
        raise InactiveInstanceError("The selected Instance is not active.")
    return instance


def connection_for(instance: InstanceConfiguration) -> Connection:
    """Resolve the connection of an Instance; a file-backed database stays inside the Database-owned storage."""
    engine = CONFIGURATION.engines[instance.engine]
    location = None
    if engine.storage_kind == "file":
        location = _contained(
            CONFIGURATION.settings.storage_root,
            instance.database,
            "the Instance database",
        )
    return Connection(
        instance.engine,
        engine.parameters,
        instance.host,
        instance.port,
        instance.database,
        instance.username,
        instance.password,
        instance.options,
        location,
    )
