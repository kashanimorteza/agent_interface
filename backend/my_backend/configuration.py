"""Settings this layer owns, and the bindings the composition declares for it.

Two different things, kept apart on purpose: what this layer decides for itself
lives in its own file, and what it consumes from another layer lives in the
project's public configuration. Neither is written into the implementation, so a
deployment can point this layer somewhere else without any of it being edited.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .faults import Misconfigured

SETTINGS_NAME = "backend.yaml"
PUBLIC_NAME = "application.yaml"
SETTINGS_VARIABLE = "MY_BACKEND_SETTINGS"
PUBLIC_VARIABLE = "MY_BACKEND_PUBLIC_CONFIGURATION"

_PACKAGE = Path(__file__).resolve().parent
_SOURCE_ROOT = _PACKAGE.parent


def settings_file() -> Path:
    """Where this layer's own settings are, wherever it is running from."""

    delivered = os.environ.get(SETTINGS_VARIABLE)
    if delivered:
        return Path(delivered).expanduser().resolve()
    beside_the_package = _SOURCE_ROOT / SETTINGS_NAME
    return beside_the_package if beside_the_package.exists() else _PACKAGE / SETTINGS_NAME


def public_file() -> Path | None:
    """Where the project's cross-layer bindings are, if they are anywhere."""

    delivered = os.environ.get(PUBLIC_VARIABLE)
    if delivered:
        return Path(delivered).expanduser().resolve()
    for directory in (_SOURCE_ROOT.parent, _SOURCE_ROOT):
        candidate = directory / PUBLIC_NAME
        if candidate.exists():
            return candidate
    return None


@dataclass(frozen=True, slots=True)
class Service:
    """Where the running layer answers."""

    host: str = "127.0.0.1"
    port: int = 8000


@dataclass(frozen=True, slots=True)
class ContractDescription:
    """Whether the contract describes itself, and where that description is."""

    enabled: bool = True
    path: str = "/openapi.json"
    human_readable_path: str = "/docs"


@dataclass(frozen=True, slots=True)
class Listing:
    """How much a listing returns."""

    default_limit: int = 50
    maximum_limit: int = 500


@dataclass(frozen=True, slots=True)
class Bindings:
    """What this layer consumes from the layers beneath it."""

    stored_identity: str | None = None


@dataclass(frozen=True, slots=True)
class Configuration:
    """Everything this layer was given, once read."""

    service: Service = field(default_factory=Service)
    description: ContractDescription = field(default_factory=ContractDescription)
    listing: Listing = field(default_factory=Listing)
    bindings: Bindings = field(default_factory=Bindings)


def _document(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text()) or {}
    if not isinstance(loaded, dict):
        raise Misconfigured(f"{path} does not hold settings")
    return loaded


def load() -> Configuration:
    """Read the layer's own settings and the bindings declared for it."""

    owned = _document(settings_file()).get("settings") or {}
    service = owned.get("service") or {}
    description = owned.get("contract_description") or {}
    listing = owned.get("listing") or {}

    public = _document(public_file())
    declared = (public.get("backend") or {}).get("bindings") or {}
    database = declared.get("database") or {}

    return Configuration(
        service=Service(
            host=service.get("host", Service.host),
            port=int(service.get("port", Service.port)),
        ),
        description=ContractDescription(
            enabled=bool(description.get("enabled", True)),
            path=description.get("path", ContractDescription.path),
            human_readable_path=description.get(
                "human_readable_path", ContractDescription.human_readable_path
            ),
        ),
        listing=Listing(
            default_limit=int(listing.get("default_limit", Listing.default_limit)),
            maximum_limit=int(listing.get("maximum_limit", Listing.maximum_limit)),
        ),
        bindings=Bindings(stored_identity=database.get("instance")),
    )


__all__ = [
    "Bindings",
    "Configuration",
    "ContractDescription",
    "Listing",
    "Service",
    "load",
    "public_file",
    "settings_file",
]
