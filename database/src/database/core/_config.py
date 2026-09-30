"""Loading and validation of the runtime configuration, the sole runtime source."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, cast

import yaml

from database.core._contracts import (
    DatabaseInstance,
    FilterCombination,
    OrderDirection,
)
from database.core._entities import entity_classes
from database.core._failures import ConfigurationFailure

CONFIGURATION_FILE = "config.yaml"
LIFECYCLE_COMMANDS = ("create_tables", "insert_initial_data")
_KEY = re.compile(r"[a-z][a-z0-9_]*")
_SECTIONS = ("engines", "instances", "settings", "initial_data")
_INSTANCE_PARTS = (
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


@dataclass(frozen=True, slots=True)
class EngineConfig:
    key: str
    name: str
    driver: str
    parameters: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class InstanceConfig:
    key: str
    name: str
    active: bool
    engine: str
    host: str | None
    port: int | None
    database: str
    username: str | None
    password: str | None
    options: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class QueryDefaults:
    filter_combination: FilterCombination
    default_limit: int
    order_field: str
    order_direction: OrderDirection


@dataclass(frozen=True, slots=True)
class AfterGeneration:
    enabled: bool
    instance: str
    fail_on_error: bool
    commands: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InitialDataSet:
    entity: str
    records: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True, slots=True)
class Configuration:
    root: Path
    storage_path: Path
    engines: Mapping[str, EngineConfig]
    instances: Mapping[str, InstanceConfig]
    default_instance: str
    query: QueryDefaults
    after_generation: AfterGeneration
    initial_data: tuple[InitialDataSet, ...]


def component_root() -> Path:
    """The Database Component root, resolved from this file's own location."""
    return Path(__file__).resolve().parents[3]


def _fail(message: str) -> ConfigurationFailure:
    return ConfigurationFailure(message)


def _mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):  # pyright: ignore[reportUnknownVariableType]
        raise _fail(f"Configuration {where} must be a mapping.")
    return value  # pyright: ignore[reportUnknownVariableType]


def _text(value: Any, where: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value):
        kind = "text" if empty else "a non-empty text value"
        raise _fail(f"Configuration {where} must be {kind}.")
    return value


def _flag(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        raise _fail(f"Configuration {where} must be true or false.")
    return value


def _integer(value: Any, where: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise _fail(f"Configuration {where} must be an integer.")
    return value


def _engines(raw: Any) -> dict[str, EngineConfig]:
    engines: dict[str, EngineConfig] = {}
    for key, part in _mapping(raw, "engines").items():
        if not _KEY.fullmatch(key):
            raise _fail(f"Engine key {key!r} is not a valid key.")
        body = _mapping(part, f"engine {key}")
        if set(body) != {"name", "driver", "parameters"}:
            raise _fail(f"Engine {key} must hold exactly name, driver, and parameters.")
        engines[key] = EngineConfig(
            key,
            _text(body["name"], f"engine {key} name"),
            _text(body["driver"], f"engine {key} driver"),
            dict(_mapping(body["parameters"], f"engine {key} parameters")),
        )
    if not engines:
        raise _fail("Configuration declares no Engine.")
    return engines


def _validate_engine_values(instance: InstanceConfig, engine: EngineConfig) -> None:
    where = f"instance {instance.key}"
    if engine.driver == "sqlite":
        _text(instance.database, f"{where} database")
    elif engine.driver == "postgresql":
        for part in ("host", "username"):
            _text(getattr(instance, part), f"{where} {part}")
        _integer(instance.port, f"{where} port")
        _text(instance.database, f"{where} database")
        _text(instance.password, f"{where} password", empty=True)
    else:
        raise _fail(f"Engine {engine.key} names an unsupported driver.")


def _instances(
    raw: Any, engines: Mapping[str, EngineConfig]
) -> dict[str, InstanceConfig]:
    instances: dict[str, InstanceConfig] = {}
    members: set[str] = set()
    names: set[str] = set()
    for key, part in _mapping(raw, "instances").items():
        if not _KEY.fullmatch(key):
            raise _fail(f"Instance key {key!r} is not a valid key.")
        body = _mapping(part, f"instance {key}")
        if set(body) != set(_INSTANCE_PARTS):
            raise _fail(f"Instance {key} must hold every Instance part and no other.")
        if key.upper() in members:
            raise _fail(f"Instance {key} collides with another Instance member.")
        members.add(key.upper())
        name = _text(body["name"], f"instance {key} name")
        if name in names:
            raise _fail(f"Instance {key} repeats another Instance name.")
        names.add(name)
        engine_key = _text(body["engine"], f"instance {key} engine")
        if engine_key not in engines:
            raise _fail(f"Instance {key} names an undeclared Engine.")
        port = body["port"]
        instance = InstanceConfig(
            key,
            name,
            _flag(body["active"], f"instance {key} active"),
            engine_key,
            None
            if body["host"] is None
            else _text(body["host"], f"instance {key} host"),
            None if port is None else _integer(port, f"instance {key} port"),
            _text(body["database"], f"instance {key} database"),
            None
            if body["username"] is None
            else _text(body["username"], f"instance {key} username"),
            None
            if body["password"] is None
            else _text(body["password"], f"instance {key} password", empty=True),
            dict(_mapping(body["options"], f"instance {key} options")),
        )
        _validate_engine_values(instance, engines[engine_key])
        instances[key] = instance
    if not instances:
        raise _fail("Configuration declares no Instance.")
    return instances


def _member[E: FilterCombination | OrderDirection](
    kind: type[E], value: Any, where: str
) -> E:
    if not isinstance(value, str) or value not in kind.__members__:
        raise _fail(f"Configuration {where} does not name a {kind.__name__} member.")
    return kind[value]


def _settings(
    raw: Any, instances: Mapping[str, InstanceConfig]
) -> tuple[str, str, QueryDefaults, AfterGeneration]:
    settings = _mapping(raw, "settings")
    if set(settings) != {"default_instance", "storage_root", "query", "lifecycle"}:
        raise _fail(
            "Settings must hold default_instance, storage_root, query, and lifecycle."
        )
    default = _text(settings["default_instance"], "settings default_instance")
    if default not in instances:
        raise _fail("The default Instance is not a declared Instance.")
    if not instances[default].active:
        raise _fail("The default Instance is not active.")
    storage_root = _text(settings["storage_root"], "settings storage_root")
    if Path(storage_root).is_absolute() or ".." in Path(storage_root).parts:
        raise _fail("The storage root must stay inside the Database Component.")
    query = _mapping(settings["query"], "settings query")
    if set(query) != {"filter_combination", "default_limit", "default_order"}:
        raise _fail(
            "Query settings hold filter_combination, default_limit, and default_order."
        )
    order = _mapping(query["default_order"], "settings query default_order")
    if set(order) != {"field", "direction"}:
        raise _fail("The default order holds field and direction.")
    limit = _integer(query["default_limit"], "settings query default_limit")
    defaults = QueryDefaults(
        _member(FilterCombination, query["filter_combination"], "filter_combination"),
        limit if limit > 0 else -1,
        _text(order["field"], "default order field"),
        _member(OrderDirection, order["direction"], "default order direction"),
    )
    lifecycle = _mapping(settings["lifecycle"], "settings lifecycle")
    if set(lifecycle) != {"after_generation"}:
        raise _fail("Lifecycle settings hold after_generation.")
    after = _mapping(lifecycle["after_generation"], "lifecycle after_generation")
    if set(after) != {"enabled", "instance", "fail_on_error", "commands"}:
        raise _fail(
            "after_generation holds enabled, instance, fail_on_error, and commands."
        )
    target = _text(after["instance"], "after_generation instance")
    target = default if target == "default_instance" else target
    if target not in instances or not instances[target].active:
        raise _fail("after_generation names an unknown or inactive Instance.")
    commands = after["commands"]
    if not isinstance(commands, list) or not all(
        isinstance(command, str) and command in LIFECYCLE_COMMANDS
        for command in commands  # pyright: ignore[reportUnknownVariableType]
    ):
        raise _fail("after_generation commands must be Lifecycle Command names.")
    return (
        default,
        storage_root,
        defaults,
        AfterGeneration(
            _flag(after["enabled"], "after_generation enabled"),
            target,
            _flag(after["fail_on_error"], "after_generation fail_on_error"),
            tuple(commands),  # pyright: ignore[reportUnknownArgumentType]
        ),
    )


def _initial_data(raw: Any) -> tuple[InitialDataSet, ...]:
    if not isinstance(raw, list):
        raise _fail("Initial Data must be a list.")
    known = entity_classes()
    sets: list[InitialDataSet] = []
    for position, part in enumerate(raw):  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
        body = _mapping(part, f"initial_data item {position}")
        if set(body) != {"entity", "records"}:
            raise _fail(f"Initial Data item {position} holds entity and records.")
        entity = _text(body["entity"], f"initial_data item {position} entity")
        if entity not in known:
            raise _fail(f"Initial Data item {position} names an unknown Entity.")
        records = body["records"]
        if not isinstance(records, list):
            raise _fail(f"Initial Data item {position} records must be a list.")
        sets.append(
            InitialDataSet(
                entity,
                tuple(
                    _mapping(record, f"initial_data item {position} record")
                    for record in cast(list[Any], records)
                ),
            )
        )
    return tuple(sets)


def _engine_files() -> set[str]:
    names: set[str] = set()
    for item in resources.files("database.engine").iterdir():
        if item.name.endswith(".py") and not item.name.startswith("_"):
            names.add(item.name.removesuffix(".py"))
    return names


def load_configuration(path: Path | None = None) -> Configuration:
    """Load, validate completely, and return the runtime configuration."""
    location = path if path is not None else component_root() / CONFIGURATION_FILE
    try:
        text = location.read_text(encoding="utf-8")
    except OSError:
        raise _fail("The runtime configuration cannot be read.") from None
    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError:
        raise _fail("The runtime configuration is not valid YAML.") from None
    body = _mapping(document, "document")
    if tuple(body) != _SECTIONS:
        raise _fail(
            "The configuration must hold engines, instances, settings, "
            "and initial_data."
        )
    engines = _engines(body["engines"])
    instances = _instances(body["instances"], engines)
    default, storage_root, query, after = _settings(body["settings"], instances)
    initial = _initial_data(body["initial_data"])
    active = {key for key, instance in instances.items() if instance.active}
    published = {member.value for member in DatabaseInstance}
    if not active <= published:
        raise _fail(
            "An active Instance has no DatabaseInstance member; regenerate Database."
        )
    if not published <= set(instances):
        raise _fail("A DatabaseInstance member names no declared Instance.")
    if _engine_files() != active:
        raise _fail(
            "Engine files do not match the active Instances; regenerate Database."
        )
    root = location.resolve().parent
    return Configuration(
        root, root / storage_root, engines, instances, default, query, after, initial
    )
