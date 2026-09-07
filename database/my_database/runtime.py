"""Resolution of the Database layer's runtime settings.

Platform owns the centralized runtime configuration and delivers each layer
its own section. Until a Platform package exists, this module performs that
delivery for the Database layer: it locates the public configuration, takes
the ``database`` section, and resolves the named secrets from the runtime
environment (the process environment first, then the project's secrets file).
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .errors import ConfigurationError

ROOT_ENV = "TRADING_ASSISTANT_ROOT"
INSTANCE_ENV = "TRADING_ASSISTANT_DATABASE_INSTANCE"
PUBLIC_CONFIG = "application.yaml"
SECRETS_FILE = ".env"
SECTION = "database"


@dataclass(frozen=True)
class InstanceSettings:
    """Everything the Storage Adapter needs to reach one Instance."""

    key: str
    name: str
    purpose: str
    engine: str
    database: str
    host: str = "localhost"
    port: int | str = "engine_default"
    username_secret: str | None = None
    password_secret: str | None = None


@dataclass(frozen=True)
class DatabaseSettings:
    """The resolved Database section plus the secrets it references."""

    project_root: Path
    default_instance: str
    storage_directory: Path
    encryption_key_secret: str
    instances: dict[str, InstanceSettings]
    bindings: dict[str, object] = field(default_factory=dict)
    secrets: Mapping[str, str] = field(default_factory=dict)

    def secret(self, name: str | None) -> str | None:
        if not name:
            return None
        value = self.secrets.get(name)
        return value or None


def find_project_root(start: Path | None = None) -> Path:
    """The directory holding the public configuration.

    Taken from the ``TRADING_ASSISTANT_ROOT`` environment variable when set,
    otherwise found by walking up from ``start`` (default: the current
    directory).
    """
    override = os.environ.get(ROOT_ENV)
    if override:
        root = Path(override).expanduser().resolve()
        if not (root / PUBLIC_CONFIG).is_file():
            raise ConfigurationError(f"{ROOT_ENV}={override} holds no {PUBLIC_CONFIG}")
        return root
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / PUBLIC_CONFIG).is_file():
            return candidate
    raise ConfigurationError(f"no {PUBLIC_CONFIG} found from {here} upwards; set {ROOT_ENV}")


def load_env_file(path: Path) -> dict[str, str]:
    """Parse a dotenv-style secrets file. Missing file yields no values."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export "):].strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


def resolve_settings(project_root: Path | None = None) -> DatabaseSettings:
    """Resolve the Database section and its secrets for this process."""
    root = project_root.resolve() if project_root else find_project_root()
    with open(root / PUBLIC_CONFIG, encoding="utf-8") as handle:
        public = yaml.safe_load(handle) or {}
    section = public.get(SECTION)
    if not isinstance(section, dict) or set(section) != {"settings", "bindings"}:
        raise ConfigurationError(f"{PUBLIC_CONFIG} has no valid {SECTION!r} section")
    settings = section["settings"] or {}
    for required in ("default_instance", "storage_directory", "encryption_key_secret", "instances"):
        if required not in settings:
            raise ConfigurationError(f"{SECTION}.settings.{required} is missing")
    instances: dict[str, InstanceSettings] = {}
    for key, raw in (settings["instances"] or {}).items():
        try:
            instances[key] = InstanceSettings(key=key, **raw)
        except TypeError as exc:
            raise ConfigurationError(f"instance {key!r}: {exc}") from exc
    if not instances:
        raise ConfigurationError("no Instance is defined")
    if settings["default_instance"] not in instances:
        raise ConfigurationError(f"default Instance {settings['default_instance']!r} is not defined")
    secrets = load_env_file(root / SECRETS_FILE)
    secrets.update({k: v for k, v in os.environ.items()})
    return DatabaseSettings(
        project_root=root,
        default_instance=settings["default_instance"],
        storage_directory=(root / settings["storage_directory"]).resolve(),
        encryption_key_secret=settings["encryption_key_secret"],
        instances=instances,
        bindings=dict(section["bindings"] or {}),
        secrets=secrets,
    )
