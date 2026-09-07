"""The settings boundary of Database.

Platform delivers the ``database`` section of the runtime configuration as
``DATABASE__<KEY>`` variables in the process environment. This module resolves
those variables — and nothing else: no configuration file and no Interface file
is read at run time — applying the resolved defaults when a value is absent.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PREFIX = "DATABASE__"
PROJECT_MARKER = ".interface"
DEFAULT_INSTANCE = "general"
DEFAULT_ENGINE = "sqlite"
DEFAULT_KEY_SECRET = "TRADING_ASSISTANT_CREDENTIAL_ENCRYPTION_KEY"
PROJECT_NAME = "Trading Assistant"


@dataclass(frozen=True)
class InstanceSettings:
    """The complete internal settings of one Instance (never published)."""

    key: str
    name: str
    purpose: str
    engine: str
    file: str | None


@dataclass(frozen=True)
class Settings:
    default: str
    instances: dict[str, InstanceSettings]
    credential_key_secret: str


BUILT_IN_INSTANCES: dict[str, InstanceSettings] = {
    DEFAULT_INSTANCE: InstanceSettings(
        key=DEFAULT_INSTANCE,
        name=f"{PROJECT_NAME} General",
        purpose="General application data.",
        engine=DEFAULT_ENGINE,
        file="database/data/trading_assistant_general.db",
    ),
}


def project_root() -> Path:
    """The directory containing ``.interface/``, found from the package location
    first and the working directory second; the working directory otherwise."""
    for start in (Path(__file__).resolve(), Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / PROJECT_MARKER).is_dir():
                return candidate
    return Path.cwd().resolve()


def resolve_path(value: str) -> Path:
    """An absolute path; a relative value is resolved against the project root."""
    path = Path(value).expanduser()
    return path if path.is_absolute() else project_root() / path


def load_settings(environ: dict[str, str] | None = None) -> Settings:
    env = os.environ if environ is None else environ
    instances = {k: v for k, v in BUILT_IN_INSTANCES.items()}
    configured: dict[str, dict[str, str]] = {}
    for variable, value in env.items():
        if not variable.startswith(PREFIX + "INSTANCES__"):
            continue
        parts = variable[len(PREFIX) + len("INSTANCES__"):].split("__", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            continue
        configured.setdefault(parts[0].lower(), {})[parts[1].lower()] = value
    for key, values in configured.items():
        base = instances.get(key) or InstanceSettings(
            key=key,
            name=f"{PROJECT_NAME} {key.replace('_', ' ').title()}",
            purpose="Configured at run time.",
            engine=DEFAULT_ENGINE,
            file=None,
        )
        instances[key] = InstanceSettings(
            key=key,
            name=base.name,
            purpose=base.purpose,
            engine=values.get("engine", base.engine).strip().lower() or base.engine,
            file=values.get("file", base.file) or base.file,
        )
    default = env.get(PREFIX + "DEFAULT_INSTANCE", DEFAULT_INSTANCE).strip().lower() or DEFAULT_INSTANCE
    secret = env.get(PREFIX + "CREDENTIAL_ENCRYPTION_KEY_SECRET", DEFAULT_KEY_SECRET).strip() or DEFAULT_KEY_SECRET
    return Settings(default=default, instances=instances, credential_key_secret=secret)


def credential_key(environ: dict[str, str] | None = None) -> str:
    """The credential-encryption secret, read from the variable named by the
    settings; raises when it is absent or empty."""
    from ..errors import CredentialKeyError

    env = os.environ if environ is None else environ
    name = load_settings(env).credential_key_secret
    value = env.get(name, "")
    if not value.strip():
        raise CredentialKeyError(
            f"the credential-encryption key is required but the environment variable {name} is not set"
        )
    return value
