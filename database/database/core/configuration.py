"""Configuration: loading and validating the Database Configuration."""

import importlib
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from .errors import ConfigurationError
from .values import FilterCombination, OrderDirection, database_instance

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
CONFIGURATION_FILE = COMPONENT_ROOT / "config.yaml"


@dataclass(frozen=True, slots=True)
class EngineConfiguration:
    """One declared Engine."""

    key: str
    name: str
    driver: str
    parameters: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class InstanceConfiguration:
    """One complete Instance definition; connection values never appear in its representation."""

    key: str
    name: str
    active: bool
    engine: str
    host: str | None = field(repr=False)
    port: int | None = field(repr=False)
    database: str = field(repr=False)
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: Mapping[str, Any] = field(repr=False)


@dataclass(frozen=True, slots=True)
class Connection:
    """The resolved connection of one Instance, handed to its Engine unit; connection values never appear in its representation."""

    instance: str
    host: str | None = field(repr=False)
    port: int | None = field(repr=False)
    database: str = field(repr=False)
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: Mapping[str, Any] = field(repr=False)
    location: Path | None = field(repr=False)


@dataclass(frozen=True, slots=True)
class QueryDefaults:
    """The configured defaults for omitted query inputs."""

    combination: FilterCombination
    limit: int
    order_field: str
    order_direction: OrderDirection


@dataclass(frozen=True, slots=True)
class Settings:
    """The component-wide runtime settings."""

    default_instance: str
    storage_root: str
    query: QueryDefaults
    after_generation_enabled: bool
    after_generation_fail_on_error: bool
    after_generation_command: str


@dataclass(frozen=True, slots=True)
class InitialDataSet:
    """The Initial Data records of one Entity."""

    entity: str
    records: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True, slots=True)
class Configuration:
    """The loaded Database Configuration."""

    engines: Mapping[str, EngineConfiguration]
    instances: Mapping[str, InstanceConfiguration]
    settings: Settings
    initial_data: tuple[InitialDataSet, ...]


def _invalid(message: str) -> ConfigurationError:
    return ConfigurationError(f"Invalid Database Configuration: {message}")


def _mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise _invalid(f"{where} must be a mapping")
    return value


def _require(mapping: Mapping[str, Any], keys: tuple[str, ...], where: str) -> None:
    for key in keys:
        if key not in mapping:
            raise _invalid(f"{where} lacks {key!r}")


def _text(value: Any, where: str, *, nullable: bool = False) -> Any:
    if value is None and nullable:
        return None
    if not isinstance(value, str):
        raise _invalid(f"{where} must be text")
    return value


def _member[E: Enum](enum: type[E], value: Any, where: str) -> E:
    if not isinstance(value, str) or value not in enum.__members__:
        raise _invalid(f"{where} must name a member of {enum.__name__}")
    return enum[value]


def _flag(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        raise _invalid(f"{where} must be true or false")
    return value


def _read(path: Path) -> Mapping[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            document = yaml.safe_load(handle)
    except OSError, yaml.YAMLError:
        raise _invalid("the configuration file cannot be read") from None
    return _mapping(document, "the configuration")


def _engines(section: Any) -> dict[str, EngineConfiguration]:
    engines: dict[str, EngineConfiguration] = {}
    for key, item in _mapping(section, "engines").items():
        where = f"engine {key!r}"
        body = _mapping(item, where)
        _require(body, ("name", "driver", "parameters"), where)
        engines[str(key)] = EngineConfiguration(
            key=str(key),
            name=_text(body["name"], f"{where} name"),
            driver=_text(body["driver"], f"{where} driver"),
            parameters=_mapping(body["parameters"], f"{where} parameters"),
        )
    return engines


def _instances(section: Any) -> dict[str, InstanceConfiguration]:
    instances: dict[str, InstanceConfiguration] = {}
    for key, item in _mapping(section, "instances").items():
        where = f"instance {key!r}"
        body = _mapping(item, where)
        _require(
            body,
            (
                "name",
                "active",
                "engine",
                "host",
                "port",
                "database",
                "username",
                "password",
                "options",
            ),
            where,
        )
        port = body["port"]
        if port is not None and (isinstance(port, bool) or not isinstance(port, int)):
            raise _invalid(f"{where} port must be a number or null")
        instances[str(key)] = InstanceConfiguration(
            key=str(key),
            name=_text(body["name"], f"{where} name"),
            active=_flag(body["active"], f"{where} active"),
            engine=_text(body["engine"], f"{where} engine"),
            host=_text(body["host"], f"{where} host", nullable=True),
            port=port,
            database=_text(body["database"], f"{where} database"),
            username=_text(body["username"], f"{where} username", nullable=True),
            password=_text(body["password"], f"{where} password", nullable=True),
            options=_mapping(body["options"], f"{where} options"),
        )
    return instances


def _settings(section: Any) -> Settings:
    body = _mapping(section, "settings")
    _require(body, ("default_instance", "storage_root", "query", "setup"), "settings")
    query = _mapping(body["query"], "settings query")
    _require(
        query,
        ("filter_combination", "default_limit", "default_order"),
        "settings query",
    )
    order = _mapping(query["default_order"], "settings default order")
    _require(order, ("field", "direction"), "settings default order")
    setup = _mapping(
        _mapping(body["setup"], "settings setup").get("after_generation"),
        "settings after-generation setup",
    )
    _require(
        setup,
        ("enabled", "fail_on_error", "command"),
        "settings after-generation setup",
    )
    limit = query["default_limit"]
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise _invalid("settings default limit must be a number")
    combination = _member(
        FilterCombination, query["filter_combination"], "settings filter combination"
    )
    direction = _member(
        OrderDirection, order["direction"], "settings default order direction"
    )
    return Settings(
        default_instance=_text(body["default_instance"], "settings default instance"),
        storage_root=_text(body["storage_root"], "settings storage root"),
        query=QueryDefaults(
            combination=combination,
            limit=limit if limit > 0 else -1,
            order_field=_text(order["field"], "settings default order field"),
            order_direction=direction,
        ),
        after_generation_enabled=_flag(
            setup["enabled"], "settings after-generation enabled"
        ),
        after_generation_fail_on_error=_flag(
            setup["fail_on_error"], "settings after-generation fail on error"
        ),
        after_generation_command=_text(
            setup["command"], "settings after-generation command"
        ),
    )


def _initial_data(section: Any) -> tuple[InitialDataSet, ...]:
    if not isinstance(section, list):
        raise _invalid("initial_data must be a list")
    sets: list[InitialDataSet] = []
    for position, item in enumerate(section, start=1):
        where = f"initial data entry {position}"
        body = _mapping(item, where)
        _require(body, ("entity", "records"), where)
        records = body["records"]
        if not isinstance(records, list):
            raise _invalid(f"{where} records must be a list")
        sets.append(
            InitialDataSet(
                entity=_text(body["entity"], f"{where} entity"),
                records=tuple(
                    _mapping(record, f"{where} record") for record in records
                ),
            )
        )
    return tuple(sets)


def _check_integrity(
    engines: Mapping[str, EngineConfiguration],
    instances: Mapping[str, InstanceConfiguration],
    settings: Settings,
) -> None:
    members: set[str] = set()
    names: set[str] = set()
    for key, instance in instances.items():
        if instance.engine not in engines:
            raise _invalid(f"instance {key!r} names an Engine that is not declared")
        member = key.upper()
        if member in members:
            raise _invalid(f"instance {key!r} repeats a public Instance identity")
        members.add(member)
        if instance.name in names:
            raise _invalid(f"instance {key!r} repeats an Instance name")
        names.add(instance.name)
    for member in database_instance:
        if member.value not in instances:
            raise _invalid(
                f"the published Instance member {member.name} names no configured Instance"
            )
    default = instances.get(settings.default_instance)
    if default is None:
        raise _invalid("the default Instance is not a configured Instance")
    if not default.active:
        raise _invalid("the default Instance is not active")


_ENGINE_PACKAGE = __name__.rsplit(".", 2)[0] + ".engine"


def engine_unit(key: str) -> Any:
    """Return the Engine unit that implements an Engine, or refuse an Engine that has none."""
    if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
        raise _invalid(f"engine {key!r} is not a valid Engine key")
    name = f"{_ENGINE_PACKAGE}.{key}"
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as error:
        if error.name != name:
            raise
        raise _invalid(f"engine {key!r} has no implementation") from None


def resolve_location(settings: Settings, instance: InstanceConfiguration) -> Path:
    """Resolve the storage location of a file-backed Instance beneath the Database storage root, or refuse an escape."""
    root = (COMPONENT_ROOT / settings.storage_root).resolve()
    if Path(settings.storage_root).is_absolute() or not root.is_relative_to(
        COMPONENT_ROOT
    ):
        raise _invalid("the storage root must lie inside the Database Component")
    location = (root / instance.database).resolve()
    if instance.database == "" or not location.is_relative_to(root) or location == root:
        raise _invalid(
            f"instance {instance.key!r} has a storage location outside the Database storage area"
        )
    return location


def connection(settings: Settings, instance: InstanceConfiguration) -> Connection:
    """Resolve the complete connection of an Instance through its Engine unit, refusing an incomplete or escaping one."""
    unit = engine_unit(instance.engine)
    for name in unit.REQUIRED:
        if getattr(instance, name) in (None, ""):
            raise _invalid(
                f"instance {instance.key!r} lacks the {name} its Engine requires"
            )
    return Connection(
        instance=instance.key,
        host=instance.host,
        port=instance.port,
        database=instance.database,
        username=instance.username,
        password=instance.password,
        options=instance.options,
        location=resolve_location(settings, instance)
        if unit.STORAGE == "file"
        else None,
    )


def load(path: Path = CONFIGURATION_FILE) -> Configuration:
    """Load the complete Database Configuration, refusing one that lacks a required section or value."""
    document = _read(path)
    _require(
        document,
        ("engines", "instances", "settings", "initial_data"),
        "the configuration",
    )
    engines = _engines(document["engines"])
    instances = _instances(document["instances"])
    settings = _settings(document["settings"])
    _check_integrity(engines, instances, settings)
    for instance in instances.values():
        if instance.active:
            connection(settings, instance)
    return Configuration(
        engines=engines,
        instances=instances,
        settings=settings,
        initial_data=_initial_data(document["initial_data"]),
    )
