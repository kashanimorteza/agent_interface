"""Bootstrap: the single entry point that reads the runtime configuration, creates the API, registers generated Groups, and serves them."""

import importlib
import pkgutil
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import groups

CONFIGURATION = Path(__file__).with_name("config.yaml")
_TEXT = ("title", "description", "key", "host", "transport_protocol", "url")
_REQUIRED = (*_TEXT, "port", "workers")


class ConfigurationError(Exception):
    """Raised when the runtime configuration or a Group registration is invalid."""


def load_configuration(path: Path = CONFIGURATION) -> dict[str, Any]:
    """Read the runtime configuration.

    Args:
        path (Path): Configuration to read.

    Returns:
        (dict[str, Any]): The configuration values, keyed by name.
    """
    try:
        values = yaml.safe_load(path.read_text())
    except (OSError, yaml.YAMLError) as error:
        raise ConfigurationError(
            f"Configuration cannot be read ({type(error).__name__})"
        ) from error
    if not isinstance(values, dict):
        raise ConfigurationError("Configuration must be a mapping of names to values")
    for name in _REQUIRED:
        if name not in values:
            raise ConfigurationError(
                f"Configuration is missing required value '{name}'"
            )
    for name in values:
        if name not in _REQUIRED:
            raise ConfigurationError(f"Configuration has unknown value '{name}'")
    for name in _TEXT:
        if not isinstance(values[name], str):
            raise ConfigurationError(f"Configuration value '{name}' must be text")
    if "/" in values["key"]:
        raise ConfigurationError("Configuration value 'key' must be one path segment")
    _check_number(values["port"], "port", 1, 65535)
    _check_number(values["workers"], "workers", 1)
    if values["url"] != base_url(values):
        raise ConfigurationError(
            f"Configuration value 'url' must equal the Base URL derived from"
            f" transport_protocol, host, port, and key ('{base_url(values)}')"
        )
    return values


def _check_number(value: Any, name: str, low: int, high: int | None = None) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigurationError(f"Configuration value '{name}' must be an integer")
    if value < low or (high is not None and value > high):
        limit = f"at least {low}" if high is None else f"between {low} and {high}"
        raise ConfigurationError(f"Configuration value '{name}' must be {limit}")


def base_url(values: dict[str, Any]) -> str:
    """Derive the Base URL from the transport protocol, host, port, and optional key.

    Args:
        values (dict[str, Any]): Configuration values.

    Returns:
        (str): The address clients use, with the key as its first path segment when set.
    """
    address = (
        f"{values['transport_protocol'].lower()}://{values['host']}:{values['port']}"
    )
    return f"{address}/{values['key']}" if values["key"] else address


def create_app(configuration: Path = CONFIGURATION) -> FastAPI:
    """Create the API boundary from the runtime configuration.

    Args:
        configuration (Path): Runtime configuration to read.

    Returns:
        (FastAPI): The API presenting the configured title and description.
    """
    values = load_configuration(configuration)
    prefix = f"/{values['key']}" if values["key"] else ""
    app = FastAPI(
        title=values["title"],
        description=values["description"],
        openapi_url=f"{prefix}/openapi.json",
        docs_url=f"{prefix}/docs",
        redoc_url=f"{prefix}/redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_groups(app, prefix)
    return app


def group_segments(names: Iterable[str]) -> list[str]:
    """Derive the URL segment of every Group from its configured name.

    Args:
        names (Iterable[str]): Configured Group names.

    Returns:
        (list[str]): One valid segment per name, unique among the names.
    """
    segments: dict[str, str] = {}
    for name in names:
        spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name.strip())
        segment = re.sub(r"[^A-Za-z0-9]+", "_", spaced).strip("_").lower()
        if not segment:
            raise ConfigurationError(
                f"Group name '{name}' does not yield a valid URL segment"
            )
        if segment in segments:
            raise ConfigurationError(
                f"Group name '{name}' collides with '{segments[segment]}' after normalization"
            )
        segments[segment] = name
    return list(segments)


def register_groups(app: FastAPI, prefix: str) -> None:
    """Register every generated Group beneath the URL Key prefix and its own URL segment.

    Args:
        app (FastAPI): API to register the Groups with.
        prefix (str): Path before the Group segment: empty, or the URL Key with a leading slash.
    """
    modules = [
        importlib.import_module(f"{groups.__name__}.{module.name}")
        for module in pkgutil.iter_modules(groups.__path__)
    ]
    for module, segment in zip(
        modules, group_segments(module.NAME for module in modules), strict=True
    ):
        app.include_router(module.router, prefix=f"{prefix}/{segment}")


def main() -> None:
    """Serve the API at the configured address."""
    values = load_configuration()
    uvicorn.run(
        "api.bootstrap:create_app",
        factory=True,
        host=values["host"],
        port=values["port"],
        workers=values["workers"],
    )
