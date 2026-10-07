import operator as operator_module
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from decimal import Decimal
from threading import Lock
from typing import Any

from sqlalchemy import (
    ColumnElement,
    Engine,
    Float,
    Table,
    UniqueConstraint,
    and_,
    cast,
    event,
    func,
    insert,
    inspect,
    or_,
    select,
    text,
    true,
)
from sqlalchemy import Connection as SqlConnection
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import exc as sql_exc
from sqlalchemy import update as sqlalchemy_update
from sqlmodel import create_engine

from database.core.configuration import Connection
from database.core.errors import ConnectionFailureError, DatabaseError, ExecutionError
from database.core.query import CheckedFilter, CheckedOrder
from database.core.values import FilterCombination, FilterOperator

ATOMIC_DDL = True

_COMPARISONS = {
    FilterOperator.EQUALS: operator_module.eq,
    FilterOperator.NOT_EQUALS: operator_module.ne,
    FilterOperator.GREATER_THAN: operator_module.gt,
    FilterOperator.GREATER_OR_EQUAL: operator_module.ge,
    FilterOperator.LESS_THAN: operator_module.lt,
    FilterOperator.LESS_OR_EQUAL: operator_module.le,
}

_engines: dict[str, Engine] = {}
_lock = Lock()


def _engine(connection: Connection) -> Engine:
    key = str(connection.path)
    with _lock:
        engine = _engines.get(key)
        if engine is None:
            if connection.path is not None:
                connection.path.parent.mkdir(parents=True, exist_ok=True)
            parameters = connection.parameters
            engine = create_engine(
                connection.url, connect_args=dict(parameters.get("connect_arguments", {}))
            )
            enforce_keys = bool(parameters.get("foreign_keys", False))

            @event.listens_for(engine, "connect")
            def _configure(dbapi_connection, _record):
                # Transactions are controlled explicitly so that schema changes are atomic too.
                dbapi_connection.isolation_level = None
                if enforce_keys:
                    dbapi_connection.execute("PRAGMA foreign_keys=ON")

            @event.listens_for(engine, "begin")
            def _begin(sql_connection):
                sql_connection.exec_driver_sql("BEGIN")

            _engines[key] = engine
        return engine


@contextmanager
def transaction(connection: Connection) -> Iterator[SqlConnection]:
    """Open the Instance's storage and run everything inside one all-or-nothing transaction."""
    name = connection.instance.name
    try:
        sql_connection = _engine(connection).connect()
    except sql_exc.DBAPIError, OSError:
        raise ConnectionFailureError(
            f"The storage of the Instance {name} cannot be reached."
        ) from None
    try:
        with sql_connection.begin():
            yield sql_connection
    except DatabaseError:
        raise
    except sql_exc.DBAPIError as error:
        raise ExecutionError(
            f"The request failed in the storage of the Instance {name}: {error.orig}"
        ) from None
    except sql_exc.SQLAlchemyError as error:
        raise ExecutionError(
            f"The request failed in the storage of the Instance {name}: {type(error).__name__}."
        ) from None
    finally:
        sql_connection.close()


def _identity(entity: type[Any]) -> str:
    return entity.declaration.primary_key


def _fetch(
    sql_connection: SqlConnection, entity: type[Any], identity: Any
) -> dict[str, Any] | None:
    table = entity.__table__
    row = sql_connection.execute(select(table).where(table.c[_identity(entity)] == identity))
    found = row.mappings().first()
    return dict(found) if found is not None else None


def add(connection: Connection, entity: type[Any], values: Mapping[str, Any]) -> dict[str, Any]:
    """Store one complete new record and return its raw stored values."""
    table = entity.__table__
    with transaction(connection) as sql_connection:
        result = sql_connection.execute(insert(table).values(**values))
        assert result.inserted_primary_key is not None
        stored = _fetch(sql_connection, entity, result.inserted_primary_key[0])
    assert stored is not None
    return stored


def update(
    connection: Connection, entity: type[Any], identity: Any, values: Mapping[str, Any]
) -> dict[str, Any] | None:
    """Replace the given mutable Field values of one record, or return nothing if absent."""
    table = entity.__table__
    with transaction(connection) as sql_connection:
        statement = sqlalchemy_update(table).where(table.c[_identity(entity)] == identity)
        if sql_connection.execute(statement.values(**values)).rowcount == 0:
            return None
        return _fetch(sql_connection, entity, identity)


def delete(connection: Connection, entity: type[Any], identity: Any) -> dict[str, Any] | None:
    """Remove one record and return its final values, or return nothing if absent."""
    table = entity.__table__
    with transaction(connection) as sql_connection:
        found = _fetch(sql_connection, entity, identity)
        if found is None:
            return None
        sql_connection.execute(
            sqlalchemy_delete(table).where(table.c[_identity(entity)] == identity)
        )
        return found


def set_active(
    connection: Connection, entity: type[Any], identity: Any, active: bool
) -> dict[str, Any] | None:
    """Set only the active state of one record and return its final values."""
    return update(connection, entity, identity, {"is_active": active})


def get_by_id(connection: Connection, entity: type[Any], identity: Any) -> dict[str, Any] | None:
    """Return the stored values of one record, or nothing if absent."""
    with transaction(connection) as sql_connection:
        return _fetch(sql_connection, entity, identity)


def _column(table: Table, name: str, kind: str) -> ColumnElement[Any]:
    column = table.c[name]
    return cast(column, Float) if kind == "decimal" else column


def _value(kind: str, value: Any) -> Any:
    return float(value) if kind == "decimal" else value


def _condition(table: Table, checked: CheckedFilter) -> ColumnElement[bool]:
    column = _column(table, checked.field, checked.type)
    operator = checked.operator
    if operator is FilterOperator.IS_NULL:
        return column.is_(None)
    if operator is FilterOperator.IS_NOT_NULL:
        return column.is_not(None)
    if operator is FilterOperator.IN:
        return column.in_([_value(checked.type, item) for item in checked.value])
    value = _value(checked.type, checked.value)
    if operator is FilterOperator.CONTAINS:
        return column.contains(value, autoescape=True)
    if operator is FilterOperator.STARTS_WITH:
        return column.startswith(value, autoescape=True)
    if operator is FilterOperator.ENDS_WITH:
        return column.endswith(value, autoescape=True)
    return _COMPARISONS[operator](column, value)


def _where(
    table: Table, filters: Sequence[CheckedFilter], combination: FilterCombination
) -> ColumnElement[bool]:
    conditions = [_condition(table, checked) for checked in filters]
    if not conditions:
        return true()
    return and_(*conditions) if combination is FilterCombination.AND else or_(*conditions)


def list_rows(
    connection: Connection,
    entity: type[Any],
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
    orders: Sequence[CheckedOrder],
    limit: int,
) -> list[dict[str, Any]]:
    """Return the matching records in the given order, up to the limit (-1 means all)."""
    table = entity.__table__
    statement = select(table).where(_where(table, filters, combination))
    for order in orders:
        column = _column(table, order.field, order.type)
        statement = statement.order_by(column.desc() if order.descending else column.asc())
    if limit > 0:
        statement = statement.limit(limit)
    with transaction(connection) as sql_connection:
        return [dict(row) for row in sql_connection.execute(statement).mappings()]


def count(
    connection: Connection,
    entity: type[Any],
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> int:
    """Return the number of matching records."""
    table = entity.__table__
    statement = select(func.count()).select_from(table).where(_where(table, filters, combination))
    with transaction(connection) as sql_connection:
        return int(sql_connection.execute(statement).scalar_one())


def _field_values(
    connection: Connection,
    entity: type[Any],
    field: str,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> list[Any]:
    table = entity.__table__
    statement = (
        select(table.c[field])
        .where(_where(table, filters, combination))
        .where(table.c[field].is_not(None))
    )
    with transaction(connection) as sql_connection:
        return list(sql_connection.execute(statement).scalars())


def sum_values(
    connection: Connection,
    entity: type[Any],
    field: Any,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Any:
    """Return the total of the non-null values; zero of the Field's kind when none match."""
    kind = field.type.value
    # Exact decimal text cannot be summed by the storage engine without losing precision.
    values = _field_values(connection, entity, field.name, filters, combination)
    if kind == "decimal":
        return sum(values, Decimal(0))
    return sum(values, 0.0 if kind == "float" else 0)


def min_value(
    connection: Connection,
    entity: type[Any],
    field: Any,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Any:
    """Return the smallest non-null value, or nothing when none match."""
    values = _field_values(connection, entity, field.name, filters, combination)
    return min(values) if values else None


def max_value(
    connection: Connection,
    entity: type[Any],
    field: Any,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Any:
    """Return the largest non-null value, or nothing when none match."""
    values = _field_values(connection, entity, field.name, filters, combination)
    return max(values) if values else None


def truncate(connection: Connection, entity: type[Any]) -> int:
    """Remove every record of the Entity, keep its Table, and return the removed count."""
    with transaction(connection) as sql_connection:
        return int(sql_connection.execute(sqlalchemy_delete(entity.__table__)).rowcount)


def execute(connection: Connection, command: str, parameters: Mapping[str, Any]) -> dict[str, Any]:
    """Run a native command with bound parameters and return its raw outcome."""
    with transaction(connection) as sql_connection:
        result = sql_connection.execute(text(command), dict(parameters))
        if result.returns_rows:
            columns = tuple(result.keys())
            rows = [dict(row) for row in result.mappings()]
            return {"rows": rows, "affected": None, "columns": columns}
        affected = result.rowcount if result.rowcount >= 0 else None
        return {"rows": None, "affected": affected, "columns": None}


def _unique_sets(table: Table) -> set[tuple[str, ...]]:
    return {
        tuple(column.name for column in constraint.columns)
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    }


def _compare(sql_connection: SqlConnection, entity: type[Any]) -> list[str]:
    """List how an existing Table differs from the Declaration-built Table; no values appear."""
    table = entity.__table__
    inspector = inspect(sql_connection)
    dialect = sql_connection.dialect
    found: list[str] = []
    columns = {column["name"]: column for column in inspector.get_columns(table.name)}
    if set(columns) != {column.name for column in table.columns}:
        return ["the set of columns differs"]
    for column in table.columns:
        stored = columns[column.name]
        if stored["nullable"] != column.nullable:
            found.append(f"column {column.name} differs in nullability")
        if stored["type"].compile(dialect).upper() != column.type.compile(dialect).upper():
            found.append(f"column {column.name} differs in type")
    primary = inspector.get_pk_constraint(table.name)["constrained_columns"]
    if tuple(primary) != tuple(column.name for column in table.primary_key.columns):
        found.append("the primary key differs")
    expected_keys = {
        (
            (key.parent.name,),
            key.column.table.name,
            (key.column.name,),
        )
        for key in table.foreign_keys
    }
    stored_keys = {
        (
            tuple(key["constrained_columns"]),
            key["referred_table"],
            tuple(key["referred_columns"]),
        )
        for key in inspector.get_foreign_keys(table.name)
    }
    if expected_keys != stored_keys:
        found.append("the relations differ")
    stored_unique = {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints(table.name)
    }
    if _unique_sets(table) != stored_unique:
        found.append("the uniqueness constraints differ")
    expected_indexes = {tuple(column.name for column in index.columns) for index in table.indexes}
    stored_indexes = {tuple(index["column_names"]) for index in inspector.get_indexes(table.name)}
    if expected_indexes != stored_indexes:
        found.append("the indexes differ")
    return found


def differences(connection: Connection, entities: Sequence[type[Any]]) -> dict[str, list[str]]:
    """Report, per Entity whose Table already exists, how the Table differs from its Declaration."""
    with transaction(connection) as sql_connection:
        existing = set(inspect(sql_connection).get_table_names())
        report = {}
        for entity in entities:
            if entity.__table__.name in existing:
                found = _compare(sql_connection, entity)
                if found:
                    report[entity.declaration.name] = found
        return report


def create_tables(connection: Connection, entities: Sequence[type[Any]]) -> int:
    """Create exactly the missing Tables of the given Entities and return how many were created."""
    with transaction(connection) as sql_connection:
        existing = set(inspect(sql_connection).get_table_names())
        missing = [entity.__table__ for entity in entities if entity.__table__.name not in existing]
        if missing:
            entities[0].metadata.create_all(sql_connection, tables=missing, checkfirst=False)
        return len(missing)


class Records:
    """Reads and inserts records inside one transaction of an Engine unit."""

    def __init__(self, sql_connection: SqlConnection) -> None:
        self._connection = sql_connection

    def find(self, entity: type[Any], criteria: Mapping[str, Any]) -> dict[str, Any] | None:
        """Return the first stored record whose Fields equal every given value."""
        table = entity.__table__
        kinds = {field.name: field.type.value for field in entity.declaration.fields}
        conditions = [
            _column(table, name, kinds[name]) == _value(kinds[name], value)
            if value is not None
            else table.c[name].is_(None)
            for name, value in criteria.items()
        ]
        row = self._connection.execute(select(table).where(and_(*conditions))).mappings().first()
        return dict(row) if row is not None else None

    def insert(self, entity: type[Any], values: Mapping[str, Any]) -> dict[str, Any]:
        """Store one record and return its stored values."""
        result = self._connection.execute(insert(entity.__table__).values(**values))
        assert result.inserted_primary_key is not None
        stored = _fetch(self._connection, entity, result.inserted_primary_key[0])
        assert stored is not None
        return stored


@contextmanager
def records(connection: Connection) -> Iterator[Records]:
    """Compare and insert records together; either every change is stored or none."""
    with transaction(connection) as sql_connection:
        yield Records(sql_connection)
