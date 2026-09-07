"""The Instance Registry published to consumers.

It derives from the validated Instance catalogue the layer declares, rather
than keeping a second catalogue of its own.
"""

from __future__ import annotations

from collections.abc import Iterator

from ..adapter.instances import Instance, InstanceCollection


class InstanceRegistry:
    """Discovery of Instance identities and the default.

    An identity taken from here can be supplied to select the Instance an
    operation or a transaction acts on. No entry carries a connection, a
    storage location, or a secret.
    """

    def __init__(self, collection: InstanceCollection) -> None:
        self._collection = collection

    @property
    def instances(self) -> tuple[Instance, ...]:
        return tuple(self._collection)

    @property
    def default(self) -> Instance:
        return self._collection.default

    def get(self, selection: str | Instance) -> Instance:
        """The identity for a declared key; an undeclared one is refused."""
        return self._collection.get(selection)

    def __iter__(self) -> Iterator[Instance]:
        return iter(self._collection)

    def __len__(self) -> int:
        return len(self._collection)

    def __contains__(self, selection: object) -> bool:
        return selection in self._collection
