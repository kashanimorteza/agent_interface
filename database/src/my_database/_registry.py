"""The public Instance Registry: selectable identities, never connections or secrets."""

from __future__ import annotations

from dataclasses import dataclass

from . import _config


@dataclass(frozen=True)
class InstanceIdentity:
    key: str
    name: str
    purpose: str


def list_instances() -> tuple[InstanceIdentity, ...]:
    return tuple(
        InstanceIdentity(key=cfg.key, name=cfg.name, purpose=cfg.purpose)
        for cfg in _config.load_instances().values()
    )


def default_instance() -> InstanceIdentity:
    key = _config.default_instance_key()
    cfg = _config.load_instances()[key]
    return InstanceIdentity(key=cfg.key, name=cfg.name, purpose=cfg.purpose)
