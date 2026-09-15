"""The public Instance Registry.

Derived from the Storage Adapter's validated runtime Instance catalogue.
Exposes every selectable Instance identity, name, and purpose together with
the one default, and never a raw connection or secret value.
"""

from __future__ import annotations

from dataclasses import dataclass

from database.adapter import StorageAdapter


@dataclass(frozen=True)
class InstanceDescriptor:
    """One publicly discoverable Instance identity."""

    key: str
    name: str
    purpose: str


class InstanceRegistry:
    """Publishes selectable Instance identities and the default, with no connection or secret exposed."""

    def __init__(self, adapter: StorageAdapter) -> None:
        self._adapter = adapter

    def list_instances(self) -> tuple[InstanceDescriptor, ...]:
        return tuple(
            InstanceDescriptor(key=i.key, name=i.name, purpose=i.purpose)
            for i in self._adapter.instances()
        )

    @property
    def default(self) -> InstanceDescriptor:
        instance = self._adapter.resolve_instance(None)
        return InstanceDescriptor(
            key=instance.key, name=instance.name, purpose=instance.purpose
        )
