"""Engine implementation for Instances stored in a SQLite file.

Only this module contains SQLite-specific behaviour.
"""

from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from decimal import Decimal
from typing import Any

from sqlalchemy import Column, and_, delete, event, func, or_, text
from sqlmodel import Session, create_engine, select

from database.configuration import Configuration, InstanceSettings
from database.contract import (
    Combination,
    CommandResult,
    Direction,
    Filter,
    Operator,
    Order,
)


def _enable_foreign_keys(connection: Any, _record: Any) -> None:
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def _column(entity_class: Any, field: Any, numeric: bool = False) -> Column[Any]:
    """Return an Entity-owned storage column, refusing an unknown or (when required) non-numeric Field."""
    columns = entity_class.__table__.columns
    field_name = getattr(field, "key", None)
    if getattr(field, "class_", None) is not entity_class or field_name not in columns:
        raise ValueError(f"Field must belong to {entity_class.__name__}")
    column = columns[field_name]
    if numeric and getattr(
        column.type, "impl_instance", column.type
    ).python_type not in (int, float, Decimal):
        raise ValueError(f"{entity_class.__name__}.{field} is not numeric")
    return column


def _condition(entity_class: Any, condition: Filter) -> Any:
    """Return the storage expression of a Filter."""
    column = _column(entity_class, condition.field)
    value = condition.value
    match condition.operator:
        case Operator.EQUALS:
            return column == value
        case Operator.NOT_EQUALS:
            return column != value
        case Operator.GREATER_THAN:
            return column > value
        case Operator.GREATER_OR_EQUAL:
            return column >= value
        case Operator.LESS_THAN:
            return column < value
        case Operator.LESS_OR_EQUAL:
            return column <= value
        case Operator.IN:
            if isinstance(value, str) or not isinstance(value, Iterable):
                raise TypeError("The 'in' operator needs a collection of values")
            return column.in_(list(value))
        case Operator.CONTAINS:
            return column.contains(value, autoescape=True)
        case Operator.STARTS_WITH:
            return column.startswith(value, autoescape=True)
        case Operator.ENDS_WITH:
            return column.endswith(value, autoescape=True)
        case Operator.IS_NULL:
            return column.is_(None)
        case Operator.IS_NOT_NULL:
            return column.is_not(None)


class Engine:
    """Carry out storage behaviour for one Instance.

    Attributes:
        instance (InstanceSettings): Instance this Engine serves.
        sql_engine (Any): Connection source for the Instance's storage.
    """

    def __init__(self, configuration: Configuration, instance: InstanceSettings):
        """Open the Instance's storage.

        Args:
            configuration (Configuration): Database Configuration that declares the Instance.
            instance (InstanceSettings): Instance to serve.
        """
        self.instance = instance
        path = configuration.storage_path(instance)
        path.parent.mkdir(parents=True, exist_ok=True)
        parameters = configuration.engines[instance.engine].parameters
        self.sql_engine = create_engine(
            f"sqlite:///{path}",
            connect_args={
                "check_same_thread": parameters.get("check_same_thread", False)
            },
        )
        if parameters.get("foreign_keys", True):
            event.listen(self.sql_engine, "connect", _enable_foreign_keys)

    @contextmanager
    def session(self) -> Iterator[Session]:
        """Open a session whose changes are committed together or not at all."""
        with (
            Session(self.sql_engine, expire_on_commit=False) as session,
            session.begin(),
        ):
            yield session

    def add(self, entity: Any) -> Any:
        """Store a new record.

        Args:
            entity (Any): Entity instance to store.

        Returns:
            (Any): The stored Entity instance, including its generated `id`.
        """
        with self.session() as session:
            session.add(entity)
            session.flush()
            session.refresh(entity)
        return entity

    def update(
        self, entity_class: Any, record_id: Any, values: Mapping[str, Any]
    ) -> Any:
        """Change the given Fields of one record.

        Args:
            entity_class (Any): Entity class of the record.
            record_id (Any): `id` of the record.
            values (Mapping[str, Any]): Field name to new value; an explicit None is stored as null.

        Returns:
            (Any): The updated Entity instance, or None when no record has that `id`.
        """
        with self.session() as session:
            record = session.get(entity_class, record_id)
            if record is None:
                return None
            for name, value in values.items():
                setattr(record, name, value)
            session.add(record)
            session.flush()
            session.refresh(record)
        return record

    def delete(self, entity_class: Any, record_id: Any) -> bool:
        """Remove one record.

        Args:
            entity_class (Any): Entity class of the record.
            record_id (Any): `id` of the record.

        Returns:
            (bool): True when a record was removed, False when none has that `id`.
        """
        with self.session() as session:
            record = session.get(entity_class, record_id)
            if record is None:
                return False
            session.delete(record)
        return True

    def _set_active(self, entity_class: Any, record_id: Any, active: bool) -> Any:
        return self.update(entity_class, record_id, {"is_active": active})

    def enable(self, entity_class: Any, record_id: Any) -> Any:
        """Set a record's `is_active` Field to true.

        Args:
            entity_class (Any): Entity class of the record.
            record_id (Any): `id` of the record.

        Returns:
            (Any): The Entity instance, or None when no record has that `id`.
        """
        return self._set_active(entity_class, record_id, True)

    def disable(self, entity_class: Any, record_id: Any) -> Any:
        """Set a record's `is_active` Field to false.

        Args:
            entity_class (Any): Entity class of the record.
            record_id (Any): `id` of the record.

        Returns:
            (Any): The Entity instance, or None when no record has that `id`.
        """
        return self._set_active(entity_class, record_id, False)

    def truncate(self, entity_class: Any) -> int:
        """Remove every record of an Entity and keep its Table structure.

        Args:
            entity_class (Any): Entity class to clear.

        Returns:
            (int): Number of records removed.
        """
        with self.session() as session:
            return session.connection().execute(delete(entity_class.__table__)).rowcount

    def get_by_id(self, entity_class: Any, record_id: Any) -> Any:
        """Return one record.

        Args:
            entity_class (Any): Entity class of the record.
            record_id (Any): `id` of the record.

        Returns:
            (Any): The Entity instance, or None when no record has that `id`.
        """
        with self.session() as session:
            return session.get(entity_class, record_id)

    def count(self, entity_class: Any) -> int:
        """Count the records of an Entity.

        Args:
            entity_class (Any): Entity class to count.

        Returns:
            (int): Number of records.
        """
        with self.session() as session:
            return session.exec(select(func.count()).select_from(entity_class)).one()

    def list_(
        self,
        entity_class: Any,
        filters: Sequence[Filter],
        combination: Combination,
        orders: Sequence[Order],
        limit: int | None,
    ) -> list[Any]:
        """Return the records of an Entity that satisfy the Filters.

        Args:
            entity_class (Any): Entity class to list.
            filters (Sequence[Filter]): Conditions on a record.
            combination (Combination): Whether a record must satisfy every Filter (AND) or any Filter (OR).
            orders (Sequence[Order]): Ordering instructions, applied in the supplied order.
            limit (int | None): Largest number of records to return, or None for every match.

        Returns:
            (list[Any]): Matching Entity instances.
        """
        statement = select(entity_class)
        if filters:
            join = and_ if combination is Combination.AND else or_
            statement = statement.where(
                join(*(_condition(entity_class, condition) for condition in filters))
            )
        for order in orders:
            column = _column(entity_class, order.field)
            statement = statement.order_by(
                column.desc()
                if order.direction is Direction.DESCENDING
                else column.asc()
            )
        if limit is not None:
            statement = statement.limit(limit)
        with self.session() as session:
            return list(session.exec(statement).all())

    def sum_(self, entity_class: Any, field: Any) -> Any:
        """Total a numeric Field, ignoring null values.

        Args:
            entity_class (Any): Entity class to total.
            field (str): Name of a numeric Field.

        Returns:
            (Any): The total, or 0 when no usable value exists.
        """
        with self.session() as session:
            total = session.exec(
                select(func.sum(_column(entity_class, field, numeric=True)))
            ).one()
        return 0 if total is None else total

    def min_(self, entity_class: Any, field: Any) -> Any:
        """Find the smallest value of a Field, ignoring null values.

        Args:
            entity_class (Any): Entity class to search.
            field (str): Name of a comparable Field.

        Returns:
            (Any): The smallest value, or None when no usable value exists.
        """
        with self.session() as session:
            return session.exec(select(func.min(_column(entity_class, field)))).one()

    def max_(self, entity_class: Any, field: Any) -> Any:
        """Find the largest value of a Field, ignoring null values.

        Args:
            entity_class (Any): Entity class to search.
            field (str): Name of a comparable Field.

        Returns:
            (Any): The largest value, or None when no usable value exists.
        """
        with self.session() as session:
            return session.exec(select(func.max(_column(entity_class, field)))).one()

    def execute_command(
        self, command: str, parameters: Mapping[str, Any] | None = None
    ) -> CommandResult:
        """Execute a SQL command in one transaction.

        Args:
            command (str): SQL command, with named `:parameter` placeholders.
            parameters (Mapping[str, Any], optional): Values for the placeholders.

        Returns:
            (CommandResult): Rows for a command that returns rows, otherwise the affected count.
        """
        with self.sql_engine.begin() as connection:
            result = connection.execute(text(command), dict(parameters or {}))
            if result.returns_rows:
                return CommandResult(
                    rows=[dict(row) for row in result.mappings()], affected_count=None
                )
            return CommandResult(rows=None, affected_count=result.rowcount)
