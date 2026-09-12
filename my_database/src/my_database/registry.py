"""Public Instance Registry.

Exposes selectable Instance identities and the configured default. Never
exposes a connection, engine object, or secret value.
"""

from __future__ import annotations

from dataclasses import dataclass

from my_database._base import get_runtime_config


@dataclass(frozen=True)
class InstanceIdentity:
    key: str
    name: str
    purpose: str


def list_instances() -> tuple[InstanceIdentity, ...]:
    config = get_runtime_config()
    return tuple(
        InstanceIdentity(key=i.key, name=i.name, purpose=i.purpose)
        for i in config.instances.values()
    )


def default_instance() -> InstanceIdentity:
    config = get_runtime_config()
    resolved = config.resolve(None)
    return InstanceIdentity(
        key=resolved.key, name=resolved.name, purpose=resolved.purpose
    )
