"""Where this layer reads the values it must never carry.

Secrets come from the layer's own private file, or from the runtime environment
for a name this layer declares. A required secret that is absent is reported as
absent, by name — never quietly replaced with something that would let the work
continue.
"""

from __future__ import annotations

import os
from pathlib import Path

from ..contract import MissingSecret
from .configuration import layer_root

ENCRYPTION_KEY = "TRADING_ASSISTANT_DATABASE_ENCRYPTION_KEY"


def secret_file() -> Path:
    """This layer's private file, beside the settings that name its secrets."""

    return layer_root() / ".env"


def _from_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        values[name.strip()] = value.strip().strip("'\"")
    return values


def resolve(name: str, *, path: Path | None = None) -> str | None:
    """The value supplied for ``name``, or ``None`` when none was.

    The runtime environment wins over the private file, so an operator can
    override one value without editing anything.
    """

    from_environment = os.environ.get(name)
    if from_environment:
        return from_environment
    return _from_file(path or secret_file()).get(name) or None


def require(name: str, *, path: Path | None = None) -> str:
    """The value supplied for ``name``, or a failure naming what is missing."""

    value = resolve(name, path=path)
    if not value:
        raise MissingSecret(
            f"{name} is required but was not supplied; add it to this layer's "
            f"private secret file or to the runtime environment"
        )
    return value


def declared_names(configuration) -> tuple[str, ...]:
    """Every secret name this layer's settings refer to."""

    names: list[str] = list(configuration.declared_secrets)
    for instance in configuration.instances.values():
        names.extend(instance.secrets.values())
        names.extend(configuration.engines[instance.engine].requires_secrets)
    return tuple(dict.fromkeys(name for name in names if name))
