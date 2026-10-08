"""The Engine unit for the SQLite Engine."""

import builtins
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from decimal import Decimal, localcontext
from typing import Any

from sqlalchemy import (
    URL,
    Integer,
    and_,
    cast,
    create_engine,
    delete,
    event,
    func,
    insert,
    inspect,
    or_,
    select,
    update,
)
from sqlalchemy import Engine as SqlEngine
from sqlalchemy.engine import Connection as SqlConnection
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from database.core.errors import (
    ConfigurationError,
    ConnectionFailureError,
    ExecutionError,
)
from database.core.values import (
    CheckedFilter,
    CheckedOrder,
    Connection,
    FilterCombination,
    FilterOperator,
)

_PRECISION = 1000


def _compare_decimals(first: str, second: str) -> int:
    a, b = Decimal(first), Decimal(second)
    return (a > b) - (a < b)


class _DecimalSum:
    """Adds decimal text values exactly and ignores null values."""

    def __init__(self) -> None:
        self.total = Decimal(0)

    def step(
        self, value: Any
    ) -> None:  # the standard library stub types the value as int; it is text or null
        if value is not None:
            with localcontext() as context:
                context.prec = _PRECISION
                self.total += Decimal(value)

    def finalize(
        self,
    ) -> Any:  # the standard library stub types the result as int; SQLite accepts text
        return str(self.total)


_BOOLEAN_ORDERING = (
    FilterOperator.GREATER_THAN,
    FilterOperator.GREATER_OR_EQUAL,
    FilterOperator.LESS_THAN,
    FilterOperator.LESS_OR_EQUAL,
)


def _column(table: Any, name: str, field_type: str) -> Any:
    column = table.c[name]
    return column.collate("DECIMAL") if field_type == "decimal" else column


def _operands(table: Any, item: CheckedFilter) -> tuple[Any, Any]:
    """Return the column and the value to compare; booleans are ordered as 0 and 1."""
    column = _column(table, item.field, item.type)
    if item.type == "boolean" and item.operator in _BOOLEAN_ORDERING:
        return cast(column, Integer), int(item.value)
    return column, item.value


def _condition(table: Any, item: CheckedFilter) -> Any:
    column, value = _operands(table, item)
    match item.operator:
        case FilterOperator.EQUALS:
            return column == value
        case FilterOperator.NOT_EQUALS:
            return column != value
        case FilterOperator.GREATER_THAN:
            return column > value
        case FilterOperator.GREATER_OR_EQUAL:
            return column >= value
        case FilterOperator.LESS_THAN:
            return column < value
        case FilterOperator.LESS_OR_EQUAL:
            return column <= value
        case FilterOperator.IN:
            return column.in_(value)
        case FilterOperator.CONTAINS:
            return column.contains(value, autoescape=True)
        case FilterOperator.STARTS_WITH:
            return column.startswith(value, autoescape=True)
        case FilterOperator.ENDS_WITH:
            return column.endswith(value, autoescape=True)
        case FilterOperator.IS_NULL:
            return column.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return column.is_not(None)


def _where(
    table: Any, filters: tuple[CheckedFilter, ...], combination: FilterCombination
) -> list[Any]:
    if not filters:
        return []
    join = and_ if combination is FilterCombination.AND else or_
    return [join(*(_condition(table, item) for item in filters))]


class Engine:
    """The SQLite implementation of every request for one Instance."""

    def __init__(self, connection: Connection) -> None:
        if connection.location is None:
            raise ConfigurationError("The SQLite Engine needs a file-backed Instance.")
        self._location = connection.location
        self._foreign_keys = bool(
            connection.parameters.get("connection", {}).get("foreign_keys", True)
        )
        self._engine: SqlEngine | None = None

    def _open(self) -> SqlEngine:
        if self._engine is None:
            try:
                self._location.parent.mkdir(parents=True, exist_ok=True)
            except OSError:
                raise ConnectionFailureError(
                    "The storage directory could not be created."
                ) from None
            engine = create_engine(
                URL.create("sqlite", database=str(self._location)),
                connect_args={"check_same_thread": False},
            )

            @event.listens_for(engine, "connect")
            def _connect(dbapi_connection: sqlite3.Connection, record: Any) -> None:
                dbapi_connection.isolation_level = None
                if self._foreign_keys:
                    dbapi_connection.execute("PRAGMA foreign_keys=ON")
                dbapi_connection.create_collation("DECIMAL", _compare_decimals)
                dbapi_connection.create_aggregate("DECIMAL_SUM", 1, _DecimalSum)

            @event.listens_for(engine, "begin")
            def _begin(connection: SqlConnection) -> None:
                connection.exec_driver_sql("BEGIN")

            self._engine = engine
        return self._engine

    @contextmanager
    def transaction(self) -> Generator[SqlConnection]:
        """Run work atomically: everything is kept when the block ends, nothing is kept when it fails."""
        failure: Exception | None = None
        try:
            with self._open().begin() as connection:
                yield connection
        except OperationalError as error:
            failure = _connection_or_execution(error)
        except IntegrityError as error:
            failure = ExecutionError(f"The operation broke a constraint: {error.orig}")
        except SQLAlchemyError:
            failure = ExecutionError(
                "The SQLite Engine could not complete the operation."
            )
        if failure is not None:
            raise failure

    def add(self, entity: type, values: dict[str, Any]) -> dict[str, Any]:
        """Store one new record and return it as stored, including generated values."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        with self.transaction() as connection:
            primary = connection.execute(
                insert(table).values(**values)
            ).inserted_primary_key
            if primary is None:
                raise ExecutionError("The record could not be stored.")
            key = primary[0]
            return dict(
                connection.execute(select(table).where(table.c.id == key))
                .mappings()
                .one()
            )

    def update(
        self, entity: type, key: int, values: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Replace the given Field values of one record; return it as stored, or None when there is none."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        with self.transaction() as connection:
            if (
                connection.execute(
                    update(table).where(table.c.id == key).values(**values)
                ).rowcount
                == 0
            ):
                return None
            return dict(
                connection.execute(select(table).where(table.c.id == key))
                .mappings()
                .one()
            )

    def delete(self, entity: type, key: int) -> dict[str, Any] | None:
        """Remove one record; return it as it was, or None when there is none."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        with self.transaction() as connection:
            row = (
                connection.execute(select(table).where(table.c.id == key))
                .mappings()
                .one_or_none()
            )
            if row is None:
                return None
            connection.execute(delete(table).where(table.c.id == key))
            return dict(row)

    def set_active(self, entity: type, key: int, active: bool) -> dict[str, Any] | None:
        """Set only the activity Field of one record; return it as stored, or None when there is none."""
        return self.update(entity, key, {"is_active": active})

    def truncate(self, entity: type) -> int:
        """Remove every record of the Entity, keep its Table, and return the removed count."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        with self.transaction() as connection:
            return connection.execute(delete(table)).rowcount

    def get(self, entity: type, key: int) -> dict[str, Any] | None:
        """Return one record by identity, or None when there is none."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        with self.transaction() as connection:
            row = (
                connection.execute(select(table).where(table.c.id == key))
                .mappings()
                .one_or_none()
            )
            return None if row is None else dict(row)

    def list(
        self,
        entity: type,
        filters: tuple[CheckedFilter, ...],
        combination: FilterCombination,
        orders: tuple[CheckedOrder, ...],
        limit: int,
    ) -> builtins.list[dict[str, Any]]:
        """Return the matching records in the given order; a limit of zero or less means no limit."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        statement = select(table).where(*_where(table, filters, combination))
        for order in orders:
            column = _column(table, order.field, order.type)
            statement = statement.order_by(
                column.desc() if order.descending else column.asc()
            )
        if limit > 0:
            statement = statement.limit(limit)
        with self.transaction() as connection:
            return [dict(row) for row in connection.execute(statement).mappings()]

    def count(
        self,
        entity: type,
        filters: tuple[CheckedFilter, ...],
        combination: FilterCombination,
    ) -> int:
        """Return the number of matching records."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        statement = (
            select(func.count())
            .select_from(table)
            .where(*_where(table, filters, combination))
        )
        with self.transaction() as connection:
            return int(connection.execute(statement).scalar_one())

    def total(
        self,
        entity: type,
        field: str,
        field_type: str,
        filters: tuple[CheckedFilter, ...],
        combination: FilterCombination,
    ) -> Any:
        """Return the total of the non-null values of a numeric Field, or zero when nothing matches."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        column = table.c[field]
        expression = (
            func.decimal_sum(column) if field_type == "decimal" else func.sum(column)
        )
        statement = (
            select(expression)
            .select_from(table)
            .where(*_where(table, filters, combination))
        )
        with self.transaction() as connection:
            value = connection.execute(statement).scalar_one()
        zero = {"integer": 0, "float": 0.0, "decimal": Decimal(0)}[field_type]
        if value is None:
            return zero
        return Decimal(value) if field_type == "decimal" else value

    def extreme(
        self,
        entity: type,
        field: str,
        field_type: str,
        largest: bool,
        filters: tuple[CheckedFilter, ...],
        combination: FilterCombination,
    ) -> Any:
        """Return the smallest or largest non-null value of a comparable Field, or None when nothing matches."""
        table = entity.__table__  # ty: ignore[unresolved-attribute]
        column = _column(table, field, field_type)
        statement = (
            select(func.max(column) if largest else func.min(column))
            .select_from(table)
            .where(*_where(table, filters, combination))
        )
        with self.transaction() as connection:
            value = connection.execute(statement).scalar_one()
        return (
            Decimal(value) if field_type == "decimal" and value is not None else value
        )

    def execute(self, command: str, parameters: Any) -> dict[str, Any]:
        """Run a native command with its bound parameters and return its raw rows, columns and affected count."""
        with self.transaction() as connection:
            result = connection.exec_driver_sql(
                command, parameters if parameters is not None else ()
            )
            if result.returns_rows:
                rows = [dict(row) for row in result.mappings()]
                return {"rows": rows, "columns": tuple(result.keys()), "affected": None}
            return {"rows": None, "columns": None, "affected": result.rowcount}

    def existing_tables(self) -> set[str]:
        """Return the names of the Tables that exist."""
        with self.transaction() as connection:
            return set(inspect(connection).get_table_names())

    def describe_table(self, name: str) -> dict[str, Any]:
        """Return the structure of an existing Table: columns, primary key, foreign keys, uniqueness, indexes."""
        with self.transaction() as connection:
            inspector = inspect(connection)
            return {
                "columns": [
                    {
                        "name": column["name"],
                        "type": type(column["type"]).__name__,
                        "length": getattr(column["type"], "length", None),
                        "nullable": column["nullable"],
                    }
                    for column in inspector.get_columns(name)
                ],
                "primary_key": list(
                    inspector.get_pk_constraint(name)["constrained_columns"]
                ),
                "foreign_keys": sorted(
                    (
                        key["constrained_columns"][0],
                        key["referred_table"],
                        key["referred_columns"][0],
                    )
                    for key in inspector.get_foreign_keys(name)
                ),
                "unique": sorted(
                    tuple(item["column_names"])
                    for item in inspector.get_unique_constraints(name)
                ),
                "indexes": sorted(
                    tuple(item["column_names"])
                    for item in inspector.get_indexes(name)
                    if not item["unique"]
                    and not str(item["name"]).startswith("sqlite_autoindex")
                ),
            }

    def create_tables(self, entities: tuple[type, ...]) -> builtins.list[str]:
        """Create exactly the Tables of the given Entities that do not exist yet, all or none; return their names."""
        tables = [entity.__table__ for entity in entities]  # ty: ignore[unresolved-attribute]
        with self.transaction() as connection:
            existing = set(inspect(connection).get_table_names())
            entities[0].metadata.create_all(connection, tables=tables, checkfirst=True)  # ty: ignore[unresolved-attribute]
        return [table.name for table in tables if table.name not in existing]

    def insert_records(
        self, records: builtins.list[tuple[type, dict[str, Any]]]
    ) -> int:
        """Insert the given records in order, all or none; return how many were inserted."""
        with self.transaction() as connection:
            for entity, values in records:
                connection.execute(insert(entity.__table__).values(**values))  # ty: ignore[unresolved-attribute]
        return len(records)


def _connection_or_execution(error: OperationalError) -> Exception:
    text = str(error.orig).lower()
    if (
        "unable to open" in text
        or "disk i/o" in text
        or "readonly" in text
        or "locked" in text
    ):
        return ConnectionFailureError("The SQLite database could not be opened.")
    return ExecutionError(
        f"The SQLite Engine could not complete the operation: {error.orig}"
    )
