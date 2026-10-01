"""Base Entity: the shared Entity-oriented Actions that every Child Service receives."""

from collections.abc import Sequence
from typing import Any, ClassVar

from logic.services.storage.interface import (
    DatabaseInstance,
    Filter,
    FilterCombination,
    Order,
    storage_add,
    storage_count,
    storage_delete,
    storage_disable,
    storage_enable,
    storage_get_by_id,
    storage_list,
    storage_max,
    storage_min,
    storage_sum,
    storage_truncate,
    storage_update,
)


class BaseEntity:
    """Entity-oriented Actions over Storage for the one Entity a Child Service is bound to.

    Attributes:
        _entity (type[Any]): The Model Entity the Child Service is bound to.
    """

    _entity: ClassVar[type[Any]]

    def _require_bound(self, entity: Any) -> None:
        if not isinstance(entity, self._entity):
            raise TypeError(
                f"{type(self).__name__} accepts only {self._entity.__name__} instances, "
                f"not {type(entity).__name__}."
            )

    def add(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Store one new instance of the bound Entity and return the stored Entity."""
        self._require_bound(entity)
        return storage_add(entity, instance)

    def update(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Replace the mutable Fields of the stored record the instance's id locates; return it or None."""
        self._require_bound(entity)
        return storage_update(entity, instance)

    def list(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Sequence[Any]:
        """Return the bound Entity's records that match; a zero or negative limit means no limit."""
        return storage_list(self._entity, filters, combination, orders, limit, instance)

    def delete(self, id: Any, instance: DatabaseInstance | None = None) -> Any:
        """Delete the record with the id and return it as it was, or None when none exists."""
        return storage_delete(self._entity, id, instance)

    def enable(self, id: Any, instance: DatabaseInstance | None = None) -> Any:
        """Set only is_active to true and return the final Entity, or None when none exists."""
        return storage_enable(self._entity, id, instance)

    def disable(self, id: Any, instance: DatabaseInstance | None = None) -> Any:
        """Set only is_active to false and return the final Entity, or None when none exists."""
        return storage_disable(self._entity, id, instance)

    def get_by_id(self, id: Any, instance: DatabaseInstance | None = None) -> Any:
        """Return the record with the id, or None when none exists."""
        return storage_get_by_id(self._entity, id, instance)

    def count(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return how many records of the bound Entity match."""
        return storage_count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls; zero when nothing matches."""
        return storage_sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return storage_min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return storage_max(self._entity, field, filters, combination, instance)

    def truncate(self, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of the bound Entity, keep its Table, and return the deleted count."""
        return storage_truncate(self._entity, instance)
