"""The public Instance Registry (Database Principle 9): consumers discover selectable Instance
identities and the default without receiving connections or secret values."""

from __future__ import annotations

import dataclasses

from database.adapter import StorageAdapter


@dataclasses.dataclass(frozen=True)
class InstanceDescriptor:
    """A published, non-secret Instance identity — no connection object or secret value."""

    key: str
    name: str
    purpose: str


class InstanceRegistry:
    """Published through the Database Interface (Database Principle 9)."""

    def __init__(self, adapter: StorageAdapter) -> None:
        self._adapter = adapter

    def list_instances(self) -> list[InstanceDescriptor]:
        return [
            InstanceDescriptor(key=instance.key, name=instance.name, purpose=instance.purpose)
            for instance in self._adapter.runtime_config.instances.values()
        ]

    @property
    def default_instance_key(self) -> str:
        return self._adapter.runtime_config.default_instance
