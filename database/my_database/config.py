"""The Database layer's own runtime configuration.

The layer owns which Engines it supports, which Instances it offers, and
which one is the default, so those live in this layer's own configuration
file inside its code path. It is located from the package itself rather than
from the process working directory, and it is validated before any data
operation is accepted.

Secret values are never held here. The configuration names a secret, and the
value is resolved from the runtime environment: the process environment
first, then the project's secrets file.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .errors import ConfigurationError

CONFIG_NAME = "database.yaml"
SECRETS_FILE = ".env"
STORAGE_DIRECTORY = "data"


def code_path() -> Path:
    """The Database layer's own directory, independent of the working directory."""
    return Path(__file__).resolve().parent.parent


def project_root() -> Path:
    """The directory holding the cross-layer configuration and the secrets file."""
    return code_path().parent


@dataclass(frozen=True)
class EngineProfile:
    """One Engine this layer implements an adapter for."""

    key: str
    storage: str
    url_scheme: str
    driver: str | None = None
    default_port: int | None = None
    foreign_keys: bool = True
    check_same_thread: bool = False
    busy_timeout_ms: int = 5000
    charset: str | None = None


@dataclass(frozen=True)
class InstanceProfile:
    """One declared Instance and the settings its connection needs."""

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
    """The validated layer configuration plus the secrets it names."""

    source: Path
    engines: dict[str, EngineProfile]
    instances: dict[str, InstanceProfile]
    default_instance: str
    encryption_key_secret: str
    secrets: Mapping[str, str] = field(default_factory=dict)

    @property
    def storage_directory(self) -> Path:
        """Where a file-backed Engine keeps its storage, inside the code path."""
        return code_path() / STORAGE_DIRECTORY

    def secret(self, name: str | None) -> str | None:
        if not name:
            return None
        return self.secrets.get(name) or None


def load_env_file(path: Path) -> dict[str, str]:
    """Parse a dotenv-style secrets file. A missing file yields no values."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


def resolve_settings(config_path: Path | None = None) -> DatabaseSettings:
    """Read and validate the layer configuration, then resolve its secrets."""
    source = Path(config_path).resolve() if config_path else code_path() / CONFIG_NAME
    if not source.is_file():
        raise ConfigurationError(f"the Database layer has no configuration at {source}")
    with open(source, encoding="utf-8") as handle:
        document = yaml.safe_load(handle) or {}
    settings = document.get("settings")
    if not isinstance(settings, dict):
        raise ConfigurationError(f"{source.name} carries no settings section")
    for forbidden in ("bindings",):
        if forbidden in document or forbidden in settings:
            raise ConfigurationError(f"{source.name} must not carry {forbidden!r}")

    engines = _engines(settings.get("engines"))
    instances = _instances(settings.get("instances"), engines)
    default_instance = settings.get("default_instance")
    if default_instance not in instances:
        raise ConfigurationError(
            f"the default Instance {default_instance!r} is not declared; "
            f"declared: {sorted(instances)}"
        )
    credentials = settings.get("credentials") or {}
    key_secret = credentials.get("encryption_key_secret")
    if not key_secret:
        raise ConfigurationError("settings.credentials.encryption_key_secret is missing")

    secrets = load_env_file(project_root() / SECRETS_FILE)
    secrets.update(os.environ)
    return DatabaseSettings(
        source=source,
        engines=engines,
        instances=instances,
        default_instance=default_instance,
        encryption_key_secret=key_secret,
        secrets=secrets,
    )


def _engines(declared: Any) -> dict[str, EngineProfile]:
    if not isinstance(declared, dict) or not declared:
        raise ConfigurationError("settings.engines declares no Engine profile")
    engines: dict[str, EngineProfile] = {}
    for key, raw in declared.items():
        try:
            engines[key] = EngineProfile(key=key, **(raw or {}))
        except TypeError as exc:
            raise ConfigurationError(f"Engine profile {key!r}: {exc}") from exc
    return engines


def _instances(declared: Any, engines: Mapping[str, EngineProfile]) -> dict[str, InstanceProfile]:
    if not isinstance(declared, dict) or not declared:
        raise ConfigurationError("settings.instances declares no Instance")
    instances: dict[str, InstanceProfile] = {}
    for key, raw in declared.items():
        try:
            profile = InstanceProfile(key=key, **(raw or {}))
        except TypeError as exc:
            raise ConfigurationError(f"Instance {key!r}: {exc}") from exc
        if profile.engine not in engines:
            raise ConfigurationError(
                f"Instance {key!r} names Engine {profile.engine!r}, which is not a declared "
                f"profile; declared: {sorted(engines)}"
            )
        instances[key] = profile
    return instances
