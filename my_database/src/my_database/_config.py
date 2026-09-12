"""Layer-local runtime configuration and secret resolution.

Non-secret settings (Engine catalogue, Instance catalogue, default selection)
live in the committed ``database.yaml`` next to this package. The
credential-encryption key never lives in a committed file: it is read from
the ``MY_DATABASE_ENCRYPTION_KEY`` environment variable, falling back to a
gitignored local file for development convenience only.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from cryptography.fernet import Fernet

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _PACKAGE_ROOT / "database.yaml"
_SECRETS_DIR = _PACKAGE_ROOT / ".secrets"
_DEV_KEY_PATH = _SECRETS_DIR / "encryption.key"
_ENCRYPTION_KEY_ENV_VAR = "MY_DATABASE_ENCRYPTION_KEY"


@dataclass(frozen=True)
class InstanceConfig:
    key: str
    name: str
    purpose: str
    engine: str
    database: str


@dataclass(frozen=True)
class RuntimeConfig:
    default_instance: str
    instances: dict[str, InstanceConfig]

    def resolve(self, instance: str | None) -> InstanceConfig:
        key = instance if instance is not None else self.default_instance
        if key not in self.instances:
            raise UnknownInstanceError(key)
        return self.instances[key]


class UnknownInstanceError(LookupError):
    def __init__(self, key: str) -> None:
        super().__init__(f"No Instance named {key!r} is configured.")
        self.key = key


def load_runtime_config() -> RuntimeConfig:
    raw = yaml.safe_load(_CONFIG_PATH.read_text(encoding="utf-8"))
    instances = {
        key: InstanceConfig(
            key=key,
            name=entry["name"],
            purpose=entry["purpose"],
            engine=entry["engine"],
            database=entry["database"],
        )
        for key, entry in raw["instances"].items()
    }
    return RuntimeConfig(default_instance=raw["default_instance"], instances=instances)


def sqlite_database_path(instance: InstanceConfig) -> Path:
    data_dir = _PACKAGE_ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / f"{instance.database}.db"


def resolve_encryption_key() -> bytes:
    """Resolve the Fernet key used for reversible credential encryption.

    Production and shared environments must supply MY_DATABASE_ENCRYPTION_KEY.
    A local, gitignored dev key is generated on first use only when that
    variable is absent, so local development never requires manual setup.
    """
    env_value = os.environ.get(_ENCRYPTION_KEY_ENV_VAR)
    if env_value:
        return env_value.encode("ascii")
    if _DEV_KEY_PATH.exists():
        return _DEV_KEY_PATH.read_bytes()
    _SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    key = Fernet.generate_key()
    _DEV_KEY_PATH.write_bytes(key)
    return key
