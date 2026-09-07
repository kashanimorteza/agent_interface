"""The Instance Registry published to consumers."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from ..adapter.instances import InstanceCollection


@dataclass(frozen=True)
class Instance:
    """One selectable database identity. Carries no connection and no secret."""

    key: str
    name: str
    purpose: str
    engine: str
    database: str
    is_default: bool


class InstanceRegistry:
    """Discovery of Instance identities and the default.

    Entries carry a key, name, purpose, Engine, and database name. No entry
    carries a connection, a storage location, or a secret. The number of
    Instances is derived from the collection.
    """

    def __init__(self, collection: InstanceCollection) -> None:
        self._collection = collection
        self._instances = {
            raw.key: Instance(
                key=raw.key,
                name=raw.name,
                purpose=raw.purpose,
                engine=raw.engine,
                database=raw.database,
                is_default=(raw.key == collection.default_key),
            )
            for raw in collection
        }

    @property
    def instances(self) -> tuple[Instance, ...]:
        return tuple(self._instances.values())

    @property
    def default(self) -> Instance:
        return self._instances[self._collection.default_key]

    def get(self, key: str) -> Instance:
        return self._instances[self._collection.resolve_key(key)]

    def __iter__(self) -> Iterator[Instance]:
        return iter(self._instances.values())

    def __len__(self) -> int:
        return len(self._instances)

    def __contains__(self, key: object) -> bool:
        return key in self._instances
