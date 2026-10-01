"""Base Entity: the one shared structure holding one Action per Storage Action that takes an Entity, in Storage's order."""

from collections.abc import Sequence
from typing import Any, ClassVar

from logic.services.storage.interface import (
    DatabaseInstance,
    Filter,
    FilterCombination,
    InvalidInputError,
    Order,
    Storage,
)


class BaseEntity:
    """Entity-oriented Actions over Storage for the one Entity a Child Service binds.

    Attributes:
        _entity (type[Any]): The Model Entity the Child Service binds.
    """

    _entity: ClassVar[type[Any]]

    def __init__(self) -> None:
        self._storage = Storage()

    def _require_bound(self, entity: Any) -> None:
        if not isinstance(entity, self._entity):
            raise InvalidInputError(
                f"{type(self).__name__} accepts only {self._entity.__name__} instances, "
                f"not {type(entity).__name__}."
            )

    def add(
        self,
        entity: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Store one complete new Entity instance and return the stored Entity, including generated values."""
        self._require_bound(entity)
        return self._storage.add(entity, instance)

    def update(
        self,
        entity: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Replace every mutable Field of the stored record the Entity's id locates; return the stored Entity or None."""
        self._require_bound(entity)
        return self._storage.update(entity, instance)

    def delete(
        self,
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Delete the record with the id and return it as it was, or None when none exists."""
        return self._storage.delete(self._entity, id, instance)

    def enable(
        self,
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Set only is_active to true and return the final Entity, or None when none exists."""
        return self._storage.enable(self._entity, id, instance)

    def disable(
        self,
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Set only is_active to false and return the final Entity, or None when none exists."""
        return self._storage.disable(self._entity, id, instance)

    def truncate(
        self,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._storage.truncate(self._entity, instance)

    def list(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Sequence[Any]:
        """Return the Entities that match, ordered and limited; a zero or negative limit means no limit."""
        return self._storage.list(
            self._entity, filters, combination, orders, limit, instance
        )

    def get_by_id(
        self,
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the Entity with the id, or None when none exists."""
        return self._storage.get_by_id(self._entity, id, instance)

    def count(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return how many Entities match."""
        return self._storage.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls; zero when nothing matches."""
        return self._storage.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return self._storage.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return self._storage.max(self._entity, field, filters, combination, instance)
