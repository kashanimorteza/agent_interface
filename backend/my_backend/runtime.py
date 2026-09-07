"""Resolution of the Backend layer's runtime settings.

Platform owns the centralized runtime configuration and delivers each layer
its own section. Until a Platform package exists, this module performs that
delivery for the Backend layer: it locates the public configuration and takes
the ``backend`` section. The Backend needs no secret of its own.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT_ENV = "TRADING_ASSISTANT_ROOT"
PUBLIC_CONFIG = "application.yaml"
SECTION = "backend"


class ConfigurationError(Exception):
    """The Backend section of the runtime configuration is missing or invalid."""


@dataclass(frozen=True)
class BackendSettings:
    project_root: Path
    host: str
    port: int
    api_documentation: bool
    model_package: str
    database_package: str
    database_instance: str | None


def find_project_root(start: Path | None = None) -> Path:
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


def resolve_settings(project_root: Path | None = None) -> BackendSettings:
    root = project_root.resolve() if project_root else find_project_root()
    with open(root / PUBLIC_CONFIG, encoding="utf-8") as handle:
        public = yaml.safe_load(handle) or {}
    section = public.get(SECTION)
    if not isinstance(section, dict) or set(section) != {"settings", "bindings"}:
        raise ConfigurationError(f"{PUBLIC_CONFIG} has no valid {SECTION!r} section")
    settings = section["settings"] or {}
    bindings = section["bindings"] or {}
    for required in ("host", "port"):
        if required not in settings:
            raise ConfigurationError(f"{SECTION}.settings.{required} is missing")
    if not isinstance(settings["port"], int):
        raise ConfigurationError(f"{SECTION}.settings.port must be an integer")
    for required in ("model", "database"):
        if not isinstance(bindings.get(required), dict) or "package" not in bindings[required]:
            raise ConfigurationError(f"{SECTION}.bindings.{required}.package is missing")
    return BackendSettings(
        project_root=root,
        host=str(settings["host"]),
        port=settings["port"],
        api_documentation=bool(settings.get("api_documentation", True)),
        model_package=bindings["model"]["package"],
        database_package=bindings["database"]["package"],
        database_instance=bindings["database"].get("instance"),
    )
