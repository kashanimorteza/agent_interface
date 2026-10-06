"""Base: the one shared structure that holds every Action of the Entity Service."""

from collections.abc import Sequence
from typing import Any

from logic.services.storage.interface import (
    DatabaseInstance,
    Filter,
    FilterCombination,
    InvalidInputError,
    Order,
    Storage,
)


class BaseEntity:
    """Every Storage Action that takes an Entity, bound to the Entity of a Child Service."""

    _entity: type  # set by each Child Service

    def __init__(self) -> None:
        self._storage = Storage()

    def _check(self, entity: Any) -> None:
        if not isinstance(entity, self._entity):
            raise InvalidInputError(f"This Child Service works on {self._entity.__name__} only")

    def add(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Store one complete new Entity instance and return the stored Entity."""
        self._check(entity)
        return self._storage.add(entity, instance)

    def update(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Replace every mutable Field of the stored record; null when no record exists."""
        self._check(entity)
        return self._storage.update(entity, instance)

    def list(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the Entities that match; a zero or negative limit means no limit."""
        return self._storage.list(self._entity, filters, combination, orders, limit, instance)

    def get_by_id(self, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Return the Entity with the given id, or null."""
        return self._storage.get_by_id(self._entity, id, instance)

    def delete(self, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Remove the record and return the final deleted Entity, or null."""
        return self._storage.delete(self._entity, id, instance)

    def enable(self, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Set only the activity Field to true and return the final Entity, or null."""
        return self._storage.enable(self._entity, id, instance)

    def disable(self, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Set only the activity Field to false and return the final Entity, or null."""
        return self._storage.disable(self._entity, id, instance)

    def count(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return self._storage.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls, or zero."""
        return self._storage.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls, or null."""
        return self._storage.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls, or null."""
        return self._storage.max(self._entity, field, filters, combination, instance)

    def truncate(self, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._storage.truncate(self._entity, instance)
