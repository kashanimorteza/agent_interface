"""Base Entity: the private shared implementation of every Entity-bound Action."""

from collections.abc import Sequence
from typing import Any, ClassVar

from logic.core.errors import EntityMismatchError
from logic.services.storage import interface as storage
from logic.services.storage.interface import DatabaseInstance


class BaseEntity:
    """Implements each Entity-bound Action once over the matching Storage Action.

    A Child Service binds one Model Entity through `entity`; the bound class is supplied to
    every class-based Storage request, so a consumer never repeats it.

    Attributes:
        entity: The Model Entity class this Child Service is bound to.
    """

    entity: ClassVar[type[Any]]

    def _check(self, entity: Any) -> None:
        if not isinstance(entity, self.entity):
            raise EntityMismatchError(
                f"{type(self).__name__} accepts only {self.entity.__name__} instances,"
                f" not {type(entity).__name__}"
            )

    def add(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist a complete Entity instance and return it with generated values."""
        self._check(entity)
        return storage.storage_add(entity, instance)

    def update(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Update the record with the Entity's id; return None when no record has it."""
        self._check(entity)
        return storage.storage_update(entity, instance)

    def list(
        self,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        orders: Sequence[Any] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Sequence[Any]:
        """Return the matching Entity instances."""
        return storage.storage_list(
            self.entity, filters, combination, orders, limit, instance
        )

    def delete(self, record_id: int, instance: DatabaseInstance | None = None) -> bool:
        """Delete a record and report whether one existed."""
        return storage.storage_delete(self.entity, record_id, instance)

    def enable(self, record_id: int, instance: DatabaseInstance | None = None) -> Any:
        """Set a record active and return it, or None when no record has the id."""
        return storage.storage_enable(self.entity, record_id, instance)

    def disable(self, record_id: int, instance: DatabaseInstance | None = None) -> Any:
        """Set a record inactive and return it, or None when no record has the id."""
        return storage.storage_disable(self.entity, record_id, instance)

    def get_by_id(
        self, record_id: int, instance: DatabaseInstance | None = None
    ) -> Any:
        """Return the record with the id, or None."""
        return storage.storage_get_by_id(self.entity, record_id, instance)

    def count(
        self,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return storage.storage_count(self.entity, filters, combination, instance)

    def sum(
        self,
        field: str,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a Field over the matching records."""
        return storage.storage_sum(self.entity, field, filters, combination, instance)

    def min(
        self,
        field: str,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest value of a Field over the matching records."""
        return storage.storage_min(self.entity, field, filters, combination, instance)

    def max(
        self,
        field: str,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest value of a Field over the matching records."""
        return storage.storage_max(self.entity, field, filters, combination, instance)

    def truncate(self, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of the bound Entity and return how many were removed."""
        return storage.storage_truncate(self.entity, instance)
