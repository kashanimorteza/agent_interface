"""Database's public entry point: the only public Database layer.

Publishes every Database Operation to Logic. Every Operation receives an
imported Entity class or Entity instance directly, never a Model name or
identity.
"""

from typing import Any, Dict, Optional, Sequence, Type, TypeVar

from sqlmodel import SQLModel

from my_database.database_data import Data

T = TypeVar("T", bound=SQLModel)


class Database:
    """The only public Database layer."""

    @staticmethod
    def add(entity: T) -> T:
        """Persist a new record for the given Entity instance and return the created record."""
        return Data.add(entity)

    @staticmethod
    def edit(entity_class: Type[T], record_id: Any) -> Optional[T]:
        """Return the record matching entity_class/record_id in editable form, or None (not found)."""
        return Data.edit(entity_class, record_id)

    @staticmethod
    def update(entity: T) -> T:
        """Persist the changed values of an Entity instance carrying its existing identifier."""
        return Data.update(entity)

    @staticmethod
    def list(
        entity_class: Type[T],
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> Sequence[T]:
        """Return every record of entity_class matching optional filters, in optional field order."""
        return Data.list(entity_class, filters, order_by)

    @staticmethod
    def delete(entity_class: Type[T], record_id: Any) -> Dict[str, bool]:
        """Remove the record matching entity_class/record_id and report the deletion outcome."""
        return Data.delete(entity_class, record_id)

    @staticmethod
    def enable(entity_class: Type[T], record_id: Any) -> Optional[T]:
        """Set the record's active indicator to enabled and return the enabled record."""
        return Data.enable(entity_class, record_id)

    @staticmethod
    def disable(entity_class: Type[T], record_id: Any) -> Optional[T]:
        """Set the record's active indicator to disabled and return the disabled record."""
        return Data.disable(entity_class, record_id)

    @staticmethod
    def get_by_id(entity_class: Type[T], record_id: Any) -> Optional[T]:
        """Return the record matching entity_class/record_id, or None (not found)."""
        return Data.get_by_id(entity_class, record_id)

    @staticmethod
    def count(entity_class: Type[SQLModel], filters: Optional[Dict[str, Any]] = None) -> int:
        """Return the number of records of entity_class matching optional filters."""
        return Data.count(entity_class, filters)

    @staticmethod
    def sum(entity_class: Type[SQLModel], field: str, filters: Optional[Dict[str, Any]] = None):
        """Return the total of one numeric field across matching records."""
        return Data.sum(entity_class, field, filters)

    @staticmethod
    def min(entity_class: Type[SQLModel], field: str, filters: Optional[Dict[str, Any]] = None):
        """Return the smallest value of one comparable field across matching records."""
        return Data.min(entity_class, field, filters)

    @staticmethod
    def max(entity_class: Type[SQLModel], field: str, filters: Optional[Dict[str, Any]] = None):
        """Return the largest value of one comparable field across matching records."""
        return Data.max(entity_class, field, filters)

    @staticmethod
    def truncate(entity_class: Type[SQLModel]) -> None:
        """Remove every record of entity_class while keeping its storage structure."""
        Data.truncate(entity_class)

    @staticmethod
    def execute_command(command: str, parameters: Optional[Dict[str, Any]] = None):
        """Execute a SQL command with optional parameters through the selected Engine."""
        return Data.execute_command(command, parameters)
