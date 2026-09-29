"""Base Entity: the private capability that implements every Entity-bound Action once.

Every Action coordinates around exactly one Storage Action reached through Storage Service
Interface. Base Entity implements no persistence and offers no Database-wide Action.
"""

from collections.abc import Sequence
from typing import Any, ClassVar

from logic.services.storage import interface as storage
from logic.services.storage.interface import DatabaseInstance


class BaseEntity:
    """Shared Entity-bound Actions; a Child Service binds one Model Entity as `entity`."""

    entity: ClassVar[type[Any]]

    @classmethod
    def _bound(cls) -> type[Any]:
        """Return the bound Model Entity class."""
        try:
            return cls.entity
        except AttributeError:
            raise TypeError(f"{cls.__name__} is not bound to a Model Entity") from None

    @classmethod
    def _require(cls, value: Any) -> None:
        """Reject a value that is not an instance of the bound Entity."""
        bound = cls._bound()
        if not isinstance(value, bound):
            raise TypeError(
                f"{cls.__name__} accepts only {bound.__name__} instances, "
                f"not {type(value).__name__}"
            )

    @classmethod
    def add(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist a complete instance of the bound Entity.

        Args:
            entity (Any): Instance of the bound Entity for the new record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The created Entity instance, including Database-generated values.

        Raises:
            TypeError: When the instance is not of the bound Entity; nothing reaches Storage.
        """
        cls._require(entity)
        return storage.storage_add(entity, instance)

    @classmethod
    def update(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Replace the mutable Fields of the record with the instance's id.

        Args:
            entity (Any): Instance of the bound Entity carrying the id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The updated Entity instance, or None when no record has that id.

        Raises:
            TypeError: When the instance is not of the bound Entity; nothing reaches Storage.
        """
        cls._require(entity)
        return storage.storage_update(entity, instance)

    @classmethod
    def list(
        cls,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        orders: Sequence[Any] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Sequence[Any]:
        """List matching records of the bound Entity.

        Args:
            filters (Sequence[Any], optional): Database Filters.
            combination (Any, optional): Database Filter Combination member.
            orders (Sequence[Any], optional): Database Orders.
            limit (int, optional): Maximum number of records; zero or less means no limit.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Sequence[Any]): The matching Entity instances.
        """
        return storage.storage_list(
            cls._bound(), filters, combination, orders, limit, instance
        )

    @classmethod
    def delete(cls, record_id: int, instance: DatabaseInstance | None = None) -> bool:
        """Delete a record of the bound Entity.

        Args:
            record_id (int): Id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (bool): True when a record was deleted and False when no record has that id.
        """
        return storage.storage_delete(cls._bound(), record_id, instance)

    @classmethod
    def enable(cls, record_id: int, instance: DatabaseInstance | None = None) -> Any:
        """Mark a record of the bound Entity active.

        Args:
            record_id (int): Id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The Entity instance, or None when no record has that id.
        """
        return storage.storage_enable(cls._bound(), record_id, instance)

    @classmethod
    def disable(cls, record_id: int, instance: DatabaseInstance | None = None) -> Any:
        """Mark a record of the bound Entity inactive.

        Args:
            record_id (int): Id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The Entity instance, or None when no record has that id.
        """
        return storage.storage_disable(cls._bound(), record_id, instance)

    @classmethod
    def get_by_id(cls, record_id: int, instance: DatabaseInstance | None = None) -> Any:
        """Retrieve one record of the bound Entity by its id.

        Args:
            record_id (int): Id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The matching Entity instance, or None when no record has that id.
        """
        return storage.storage_get_by_id(cls._bound(), record_id, instance)

    @classmethod
    def count(
        cls,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Count matching records of the bound Entity.

        Args:
            filters (Sequence[Any], optional): Database Filters.
            combination (Any, optional): Database Filter Combination member.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (int): The number of matching records.
        """
        return storage.storage_count(cls._bound(), filters, combination, instance)

    @classmethod
    def sum(
        cls,
        field: str,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Total a Field of the bound Entity over matching records.

        Args:
            field (str): Name of the Entity Field.
            filters (Sequence[Any], optional): Database Filters.
            combination (Any, optional): Database Filter Combination member.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): That Field's total, or zero when no usable value exists.
        """
        return storage.storage_sum(cls._bound(), field, filters, combination, instance)

    @classmethod
    def min(
        cls,
        field: str,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Find the smallest value of a Field of the bound Entity over matching records.

        Args:
            field (str): Name of the Entity Field.
            filters (Sequence[Any], optional): Database Filters.
            combination (Any, optional): Database Filter Combination member.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The smallest usable value, or None when none exists.
        """
        return storage.storage_min(cls._bound(), field, filters, combination, instance)

    @classmethod
    def max(
        cls,
        field: str,
        filters: Sequence[Any] | None = None,
        combination: Any | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Find the largest value of a Field of the bound Entity over matching records.

        Args:
            field (str): Name of the Entity Field.
            filters (Sequence[Any], optional): Database Filters.
            combination (Any, optional): Database Filter Combination member.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The largest usable value, or None when none exists.
        """
        return storage.storage_max(cls._bound(), field, filters, combination, instance)

    @classmethod
    def truncate(cls, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of the bound Entity.

        Args:
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (int): The number of deleted records.
        """
        return storage.storage_truncate(cls._bound(), instance)
