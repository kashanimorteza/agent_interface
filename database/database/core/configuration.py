"""Load and validate the Database Configuration, the sole runtime source.

Runtime never reads the Database Preferences. Every value here comes from the generated
configuration, and a failure names the item at fault but never shows a connection value.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from database.core.errors import ConfigurationError
from database.core.values import DatabaseInstance, FilterCombination, OrderDirection

# The Database Component: the directory that holds the configuration, storage, and project file.
COMPONENT_ROOT = Path(__file__).resolve().parents[2]
CONFIGURATION_FILE = "config.yaml"
_INSTALLED_PARTS = {"site-packages", "dist-packages", ".venv"}


@dataclass(frozen=True, slots=True)
class EngineConfig:
    key: str
    name: str
    driver: str
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
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

    @property
    def member(self) -> str:
        """The name of this Instance's DatabaseInstance member."""
        return self.key.upper()


@dataclass(frozen=True, slots=True)
class DefaultOrder:
    field: str
    direction: OrderDirection


@dataclass(frozen=True, slots=True)
class QueryDefaults:
    filter_combination: FilterCombination
    default_limit: int
    default_order: DefaultOrder


@dataclass(frozen=True, slots=True)
class AfterGeneration:
    enabled: bool
    fail_on_error: bool
    command: str


@dataclass(frozen=True, slots=True)
class Settings:
    default_instance: str
    storage_root: str
    query: QueryDefaults
    after_generation: AfterGeneration


@dataclass(frozen=True, slots=True)
class InitialDataGroup:
    entity: str
    records: tuple[dict[str, Any], ...]


@dataclass(frozen=True, slots=True)
class Configuration:
    root: Path
    engines: dict[str, EngineConfig]
    instances: dict[str, InstanceConfig]
    settings: Settings
    initial_data: tuple[InitialDataGroup, ...]


@dataclass(frozen=True, slots=True)
class Connection:
    """What an Engine unit receives for one Instance; it is never published."""

    engine: EngineConfig
    instance: InstanceConfig
    storage_root: Path


def connection_for(configuration: Configuration, key: str) -> Connection:
    """Build the connection of one Instance, with the storage root resolved inside the Database."""
    root = configuration.root
    storage_root = (root / configuration.settings.storage_root).resolve()
    if not storage_root.is_relative_to(root):
        raise ConfigurationError(
            "Invalid Database Configuration: the storage root escapes the Database"
        )
    instance = configuration.instances[key]
    return Connection(configuration.engines[instance.engine], instance, storage_root)


def _fail(message: str) -> ConfigurationError:
    return ConfigurationError(f"Invalid Database Configuration: {message}")


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _fail(f"{where} must be a mapping")
    return value


def _text(mapping: dict[str, Any], key: str, where: str, *, nullable: bool = False) -> Any:
    if key not in mapping:
        raise _fail(f"{where} is missing {key}")
    value = mapping[key]
    if value is None and nullable:
        return None
    if not isinstance(value, str) or (not nullable and value == ""):
        raise _fail(f"{where}.{key} must be text")
    return value


def _flag(mapping: dict[str, Any], key: str, where: str) -> bool:
    if key not in mapping or not isinstance(mapping[key], bool):
        raise _fail(f"{where}.{key} must be true or false")
    return mapping[key]


def _member(enum: Any, name: Any, where: str) -> Any:
    if not isinstance(name, str) or name not in enum.__members__:
        raise _fail(f"{where} does not name a member of {enum.__name__}")
    return enum[name]


def _engines(raw: Any) -> dict[str, EngineConfig]:
    engines = _mapping(raw, "engines")
    if not engines:
        raise _fail("engines is empty")
    result: dict[str, EngineConfig] = {}
    for key, value in engines.items():
        where = f"engines.{key}"
        entry = _mapping(value, where)
        result[key] = EngineConfig(
            key=key,
            name=_text(entry, "name", where),
            driver=_text(entry, "driver", where),
            parameters=_mapping(entry.get("parameters"), f"{where}.parameters"),
        )
    return result


def _instances(raw: Any, engines: dict[str, EngineConfig]) -> dict[str, InstanceConfig]:
    instances = _mapping(raw, "instances")
    if not instances:
        raise _fail("instances is empty")
    result: dict[str, InstanceConfig] = {}
    for key, value in instances.items():
        where = f"instances.{key}"
        entry = _mapping(value, where)
        port = entry.get("port", ...)
        if port is ... or (
            port is not None and (isinstance(port, bool) or not isinstance(port, int))
        ):
            raise _fail(f"{where}.port must be a number or null")
        for required in ("host", "username", "password"):
            if required not in entry:
                raise _fail(f"{where} is missing {required}")
        engine = _text(entry, "engine", where)
        if engine not in engines:
            raise _fail(f"{where} names an Engine that is not declared")
        result[key] = InstanceConfig(
            key=key,
            name=_text(entry, "name", where),
            active=_flag(entry, "active", where),
            engine=engine,
            host=_text(entry, "host", where, nullable=True),
            port=port,
            database=_text(entry, "database", where),
            username=_text(entry, "username", where, nullable=True),
            password=_text(entry, "password", where, nullable=True),
            options=_mapping(entry.get("options"), f"{where}.options"),
        )
    names = [instance.name for instance in result.values()]
    members = [instance.member for instance in result.values()]
    if len(set(names)) != len(names) or len(set(members)) != len(members):
        raise _fail("an Instance name or DatabaseInstance member is repeated")
    return result


def _settings(raw: Any, instances: dict[str, InstanceConfig]) -> Settings:
    settings = _mapping(raw, "settings")
    default = _text(settings, "default_instance", "settings")
    if default not in instances or not instances[default].active:
        raise _fail("settings.default_instance must name an active Instance")
    storage_root = _text(settings, "storage_root", "settings")
    parts = Path(storage_root).parts
    if Path(storage_root).is_absolute() or ".." in parts:
        raise _fail("settings.storage_root must stay inside the Database")
    query = _mapping(settings.get("query"), "settings.query")
    limit = query.get("default_limit")
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise _fail("settings.query.default_limit must be a number")
    order = _mapping(query.get("default_order"), "settings.query.default_order")
    lifecycle = _mapping(settings.get("lifecycle"), "settings.lifecycle")
    after = _mapping(lifecycle.get("after_generation"), "settings.lifecycle.after_generation")
    command = _text(after, "command", "settings.lifecycle.after_generation")
    if command != "prepare":
        raise _fail("settings.lifecycle.after_generation.command must be prepare")
    return Settings(
        default_instance=default,
        storage_root=storage_root,
        query=QueryDefaults(
            filter_combination=_member(
                FilterCombination,
                query.get("filter_combination"),
                "settings.query.filter_combination",
            ),
            default_limit=-1 if limit <= 0 else limit,
            default_order=DefaultOrder(
                field=_text(order, "field", "settings.query.default_order"),
                direction=_member(
                    OrderDirection, order.get("direction"), "settings.query.default_order.direction"
                ),
            ),
        ),
        after_generation=AfterGeneration(
            enabled=_flag(after, "enabled", "settings.lifecycle.after_generation"),
            fail_on_error=_flag(after, "fail_on_error", "settings.lifecycle.after_generation"),
            command=command,
        ),
    )


def _initial_data(raw: Any) -> tuple[InitialDataGroup, ...]:
    if not isinstance(raw, list):
        raise _fail("initial_data must be a list")
    groups = []
    for index, value in enumerate(raw):
        where = f"initial_data[{index}]"
        entry = _mapping(value, where)
        records = entry.get("records")
        if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
            raise _fail(f"{where}.records must be a list of mappings")
        groups.append(InitialDataGroup(_text(entry, "entity", where), tuple(records)))
    return tuple(groups)


def load_configuration(root: Path | None = None) -> Configuration:
    """Read and validate the generated configuration of the Database Component."""
    root = (root or COMPONENT_ROOT).resolve()
    if _INSTALLED_PARTS & set(root.parts) or not (root / "pyproject.toml").is_file():
        raise _fail("the Database must run from its own Component, not from an installed copy")
    path = root / CONFIGURATION_FILE
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise _fail("the configuration cannot be read") from error
    document = _mapping(document, "the configuration")
    for section in ("engines", "instances", "settings", "initial_data"):
        if section not in document:
            raise _fail(f"{section} is missing")
    engines = _engines(document["engines"])
    instances = _instances(document["instances"], engines)
    settings = _settings(document["settings"], instances)
    active = {instance.member for instance in instances.values() if instance.active}
    if active != {member.name for member in DatabaseInstance}:
        raise _fail("DatabaseInstance members do not match the active Instances; regenerate")
    return Configuration(
        root, engines, instances, settings, _initial_data(document["initial_data"])
    )
