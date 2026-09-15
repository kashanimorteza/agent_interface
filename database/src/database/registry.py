"""Public Instance Registry.

Publishes selectable Instance identities and the default, derived from the
validated runtime Instance catalogue. Never exposes a connection or secret.
"""

from __future__ import annotations

from dataclasses import dataclass

from database.config import StorageConfig, load_storage_config


@dataclass(frozen=True, slots=True)
class InstanceIdentity:
    key: str
    name: str
    purpose: str


@dataclass(frozen=True, slots=True)
class InstanceRegistry:
    instances: tuple[InstanceIdentity, ...]
    default: str

    def get(self, key: str | None = None) -> InstanceIdentity:
        target = key or self.default
        for identity in self.instances:
            if identity.key == target:
                return identity
        from database.exceptions import UnknownInstanceError

        raise UnknownInstanceError(f"Unknown Instance {target!r}")


def instance_registry(config: StorageConfig | None = None) -> InstanceRegistry:
    cfg = config or load_storage_config()
    identities = tuple(
        InstanceIdentity(key=inst.key, name=inst.name, purpose=inst.purpose)
        for inst in cfg.instances.values()
    )
    return InstanceRegistry(instances=identities, default=cfg.default_instance)
