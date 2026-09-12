"""The public Instance Registry: discoverable Instance identities and the default.

Exposes no raw connection object and no secret value.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import _session


@dataclass(frozen=True)
class InstanceIdentity:
    """One publicly discoverable Instance identity."""

    key: str
    name: str
    purpose: str


def list_instances() -> list[InstanceIdentity]:
    """List every configured Instance identity."""
    config = _session.get_config()
    return [
        InstanceIdentity(key=instance.key, name=instance.name, purpose=instance.purpose)
        for instance in config.instances.values()
    ]


def default_instance() -> InstanceIdentity:
    """The Instance identity used when a consumer omits an explicit selection."""
    config = _session.get_config()
    instance = config.resolve(None)
    return InstanceIdentity(key=instance.key, name=instance.name, purpose=instance.purpose)
