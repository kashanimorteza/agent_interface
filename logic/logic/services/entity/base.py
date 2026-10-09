"""The Entity Service Base: every Action, shared by every Child Service."""

from collections.abc import Sequence
from typing import Any, ClassVar

from database.interface import database_error, database_interface


class BaseEntity:
    """The one shared structure holding the Database object and every Action."""

    _entity: ClassVar[type]

    def __init__(self) -> None:
        self._database = database_interface()

    def _require_bound(self, entity: Any) -> None:
        if not isinstance(entity, self._entity):
            raise database_error.InvalidInputError(
                f"An instance of {self._entity.__name__} is required"
            )

    def add(self, entity: Any, instance: Any = None) -> Any:
        """Store one new Entity instance and return the stored Entity, including generated values."""
        self._require_bound(entity)
        return self._database.add(entity, instance)

    def update(self, entity: Any, instance: Any = None) -> Any:
        """Replace every mutable Field of the stored record of an Entity instance; None when it does not exist."""
        self._require_bound(entity)
        return self._database.update(entity, instance)

    def list(
        self,
        filters: Any = None,
        combination: Any = None,
        orders: Any = None,
        limit: Any = None,
        instance: Any = None,
    ) -> Sequence[Any]:
        """Return the matching Entity instances; a zero or negative limit means no limit."""
        return self._database.list(
            self._entity, filters, combination, orders, limit, instance
        )

    def get_by_id(self, id: Any, instance: Any = None) -> Any:
        """Return the Entity with that id, or None when no record exists."""
        return self._database.get_by_id(self._entity, id, instance)

    def delete(self, id: Any, instance: Any = None) -> Any:
        """Remove the record and return the deleted Entity, or None when no record exists."""
        return self._database.delete(self._entity, id, instance)

    def enable(self, id: Any, instance: Any = None) -> Any:
        """Set only is_active to true and return the final Entity, or None when no record exists."""
        return self._database.enable(self._entity, id, instance)

    def disable(self, id: Any, instance: Any = None) -> Any:
        """Set only is_active to false and return the final Entity, or None when no record exists."""
        return self._database.disable(self._entity, id, instance)

    def count(
        self,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> int:
        """Return the number of matching records."""
        return self._database.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring null values, or zero when nothing matches."""
        return self._database.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> Any:
        """Return the smallest non-null value of a comparable Field, or None when nothing matches."""
        return self._database.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Any = None,
        combination: Any = None,
        instance: Any = None,
    ) -> Any:
        """Return the largest non-null value of a comparable Field, or None when nothing matches."""
        return self._database.max(self._entity, field, filters, combination, instance)

    def truncate(self, instance: Any = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._database.truncate(self._entity, instance)
