"""SQLite Engine unit: every storage behavior that needs the driver."""

import sqlite3
from collections.abc import Callable, Generator, Sequence
from contextlib import contextmanager
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, event
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlmodel import (
    and_,
    create_engine,
    delete,
    func,
    insert,
    inspect,
    or_,
    select,
    update,
)

from database.core.errors import (
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DeclarationMismatchError,
    ExecutionError,
)
from database.core.values import (
    CheckedFilter,
    CheckedOrder,
    Connection,
    FilterCombination,
    FilterOperator,
)

_ENGINES: dict[Path, Engine] = {}


def _compare_decimals(left: str, right: str) -> int:
    """Order two stored decimal texts by their exact numeric value."""
    first, second = Decimal(left), Decimal(right)
    return (first > second) - (first < second)


def _prepare_connection(
    foreign_keys: bool,
) -> Callable[[sqlite3.Connection, Any], None]:
    def prepare(dbapi_connection: sqlite3.Connection, _record: Any) -> None:
        dbapi_connection.isolation_level = None
        dbapi_connection.create_collation("DECIMAL", _compare_decimals)
        if foreign_keys:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.close()

    return prepare


def engine_of(connection: Connection) -> Engine:
    """Return the open SQLAlchemy engine of an Instance's Database-owned file."""
    path = connection.storage_path
    if path is None:
        raise ConfigurationError(
            f"Instance {connection.instance!r} is not backed by a storage file"
        )
    engine = _ENGINES.get(path)
    if engine is None:
        foreign_keys = bool(
            connection.parameters.get("connection", {}).get("foreign_keys", False)
        )
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            raise ConnectionFailureError(
                f"Instance {connection.instance!r} storage cannot be created"
            ) from None
        engine = create_engine(
            f"sqlite:///{path}", connect_args={"check_same_thread": False}
        )
        event.listen(engine, "connect", _prepare_connection(foreign_keys))
        event.listen(engine, "begin", lambda cx: cx.exec_driver_sql("BEGIN"))
        _ENGINES[path] = engine
    try:
        with engine.connect():
            pass
    except OperationalError, OSError:
        raise ConnectionFailureError(
            f"Cannot connect to Instance {connection.instance!r}"
        ) from None
    return engine


@contextmanager
def failures(connection: Connection, action: str) -> Generator[None]:
    """Report any storage failure as a Database error without exposing values."""
    try:
        yield
    except DatabaseError:
        raise
    except SQLAlchemyError, sqlite3.Error, ValueError:
        raise ExecutionError(
            f"{action} failed on Instance {connection.instance!r}"
        ) from None


_PYTHON_TYPES = {
    "string": str,
    "integer": int,
    "float": float,
    "decimal": str,
    "boolean": bool,
    "datetime": datetime,
    "date": date,
    "time": time,
}


def _differences(inspector: Any, entity: Any, names: dict[str, str]) -> list[str]:
    """Return how the existing Table of the Entity differs from its Declaration."""
    declaration = entity.declaration
    table = entity.__name__
    found = []
    columns = inspector.get_columns(table)
    if [column["name"] for column in columns] != [f.name for f in declaration.fields]:
        return ["the Fields differ"]
    for column, spec in zip(columns, declaration.fields, strict=True):
        expected = _PYTHON_TYPES.get(spec.type.value)
        if expected is not None and column["type"].python_type is not expected:
            found.append(f"the Type of {spec.name!r} differs")
        if (
            bool(column["nullable"]) != spec.nullable
            and spec.name != declaration.primary_key
        ):
            found.append(f"the nullability of {spec.name!r} differs")
    if inspector.get_pk_constraint(table)["constrained_columns"] != [
        declaration.primary_key
    ]:
        found.append("the Primary Key differs")
    relations = {
        ((r.local_field,), names[r.target_entity], (r.target_field,))
        for r in declaration.relations
    }
    reflected = {
        (
            tuple(f["constrained_columns"]),
            f["referred_table"],
            tuple(f["referred_columns"]),
        )
        for f in inspector.get_foreign_keys(table)
    }
    if relations != reflected:
        found.append("the Relations differ")
    unique = {tuple(entry) for entry in declaration.unique_constraints}
    if unique != {
        tuple(u["column_names"]) for u in inspector.get_unique_constraints(table)
    }:
        found.append("the Uniqueness Constraints differ")
    indexes = {tuple(entry) for entry in declaration.indexes}
    if indexes != {tuple(i["column_names"]) for i in inspector.get_indexes(table)}:
        found.append("the Indexes differ")
    return found


def create_tables(connection: Connection, entities: Sequence[Any]) -> int:
    """Create the missing Tables of the Entities; return how many were created."""
    engine = engine_of(connection)
    names = {entity.declaration.name: entity.__name__ for entity in entities}
    with failures(connection, "Table creation"):
        inspector = inspect(engine)
        existing = set(inspector.get_table_names())
        for entity in entities:
            if entity.__name__ in existing:
                found = _differences(inspector, entity, names)
                if found:
                    raise DeclarationMismatchError(
                        f"Table {entity.__name__!r} differs from its Entity: "
                        + "; ".join(found)
                    )
        missing = [
            entity.__table__ for entity in entities if entity.__name__ not in existing
        ]
        if missing:
            with engine.begin() as cx:
                entities[0].metadata.create_all(cx, tables=missing, checkfirst=False)
    return len(missing)


def execute_command(
    connection: Connection, command: str, parameters: Any
) -> tuple[tuple[dict[str, Any], ...] | None, int | None, tuple[str, ...] | None]:
    """Run a native command; return its rows, affected count, and columns."""
    engine = engine_of(connection)
    with failures(connection, "Command"), engine.begin() as cx:
        result = cx.exec_driver_sql(
            command, parameters if parameters is not None else ()
        )
        if result.returns_rows:
            columns = tuple(result.keys())
            return tuple(dict(row._mapping) for row in result), None, columns
        return None, result.rowcount, None


def _expression(table: Any, name: str, type_name: str) -> Any:
    """The column, ordered by exact numeric value when it holds a decimal."""
    column = table.c[name]
    return column.collate("DECIMAL") if type_name == "decimal" else column


def _condition(table: Any, item: CheckedFilter) -> Any:
    expression = _expression(table, item.field, item.type)
    value = item.value
    match item.operator:
        case FilterOperator.EQUALS:
            return expression == value
        case FilterOperator.NOT_EQUALS:
            return expression != value
        case FilterOperator.GREATER_THAN:
            return expression > value
        case FilterOperator.GREATER_OR_EQUAL:
            return expression >= value
        case FilterOperator.LESS_THAN:
            return expression < value
        case FilterOperator.LESS_OR_EQUAL:
            return expression <= value
        case FilterOperator.IN:
            return expression.in_(value)
        case FilterOperator.CONTAINS:
            return expression.contains(value, autoescape=True)
        case FilterOperator.STARTS_WITH:
            return expression.startswith(value, autoescape=True)
        case FilterOperator.ENDS_WITH:
            return expression.endswith(value, autoescape=True)
        case FilterOperator.IS_NULL:
            return expression.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return expression.is_not(None)


def _where(
    table: Any, filters: Sequence[CheckedFilter], combination: FilterCombination
) -> list[Any]:
    if not filters:
        return []
    combine = and_ if combination is FilterCombination.AND else or_
    return [combine(*(_condition(table, item) for item in filters))]


def _row(row: Any) -> dict[str, Any]:
    return dict(row._mapping)


def add(connection: Connection, entity: Any, values: dict[str, Any]) -> dict[str, Any]:
    """Store one new record and return the stored row."""
    table = entity.__table__
    with failures(connection, "Add"), engine_of(connection).begin() as cx:
        key = cx.execute(insert(table).values(**values)).inserted_primary_key
        if key is None:
            raise ExecutionError(
                f"Add stored no record on Instance {connection.instance!r}"
            )
        return _row(cx.execute(select(table).where(table.c.id == key[0])).one())


def replace(
    connection: Connection, entity: Any, identity: Any, values: dict[str, Any]
) -> dict[str, Any] | None:
    """Replace the given Fields of a record; nothing when no record exists."""
    table = entity.__table__
    statement = update(table).where(table.c.id == identity).values(**values)
    with failures(connection, "Update"), engine_of(connection).begin() as cx:
        if cx.execute(statement).rowcount == 0:
            return None
        return _row(cx.execute(select(table).where(table.c.id == identity)).one())


def get_by_id(
    connection: Connection, entity: Any, identity: Any
) -> dict[str, Any] | None:
    """Return the row with the identity, or nothing."""
    table = entity.__table__
    with failures(connection, "Get"), engine_of(connection).connect() as cx:
        row = cx.execute(select(table).where(table.c.id == identity)).first()
        return None if row is None else _row(row)


def list_rows(
    connection: Connection,
    entity: Any,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
    orders: Sequence[CheckedOrder],
    limit: int,
) -> list[dict[str, Any]]:
    """Return the matching rows in the given order, at most limit when positive."""
    table = entity.__table__
    statement = select(table).where(*_where(table, filters, combination))
    for order in orders:
        expression = _expression(table, order.field, order.type)
        statement = statement.order_by(
            expression.desc() if order.descending else expression.asc()
        )
    if limit > 0:
        statement = statement.limit(limit)
    with failures(connection, "List"), engine_of(connection).connect() as cx:
        return [_row(row) for row in cx.execute(statement)]


def count(
    connection: Connection,
    entity: Any,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> int:
    """Return how many rows match."""
    table = entity.__table__
    statement = (
        select(func.count())
        .select_from(table)
        .where(*_where(table, filters, combination))
    )
    with failures(connection, "Count"), engine_of(connection).connect() as cx:
        return int(cx.execute(statement).scalar_one())


def total(
    connection: Connection,
    entity: Any,
    field: tuple[str, str],
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> int | float | Decimal:
    """Return the sum of a numeric Field, ignoring nulls; zero when nothing matches."""
    table = entity.__table__
    name, type_name = field
    where = _where(table, filters, combination)
    with failures(connection, "Sum"), engine_of(connection).connect() as cx:
        if type_name == "decimal":
            rows = cx.execute(
                select(table.c[name]).where(table.c[name].is_not(None), *where)
            )
            return sum((value for (value,) in rows), Decimal(0))
        result = cx.execute(select(func.sum(table.c[name])).where(*where)).scalar_one()
    return result if result is not None else (0.0 if type_name == "float" else 0)


def extreme(
    connection: Connection,
    entity: Any,
    field: tuple[str, str],
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
    largest: bool,
) -> Any:
    """Return the smallest or largest non-null value of a Field, or nothing."""
    table = entity.__table__
    name, type_name = field
    aggregate = func.max if largest else func.min
    statement = select(aggregate(_expression(table, name, type_name))).where(
        table.c[name].is_not(None), *_where(table, filters, combination)
    )
    with failures(connection, "Aggregate"), engine_of(connection).connect() as cx:
        return cx.execute(statement).scalar_one()


def remove(connection: Connection, entity: Any, identity: Any) -> dict[str, Any] | None:
    """Delete one record and return it; nothing when no record exists."""
    table = entity.__table__
    with failures(connection, "Delete"), engine_of(connection).begin() as cx:
        row = cx.execute(select(table).where(table.c.id == identity)).first()
        if row is None:
            return None
        cx.execute(delete(table).where(table.c.id == identity))
        return _row(row)


def set_active(
    connection: Connection, entity: Any, identity: Any, active: bool
) -> dict[str, Any] | None:
    """Set only the activity Field and return the final row; nothing when absent."""
    table = entity.__table__
    statement = update(table).where(table.c.id == identity).values(is_active=active)
    with failures(connection, "Activation"), engine_of(connection).begin() as cx:
        if cx.execute(statement).rowcount == 0:
            return None
        return _row(cx.execute(select(table).where(table.c.id == identity)).one())


def truncate(connection: Connection, entity: Any) -> int:
    """Remove every record of the Entity, keep its Table, and return the count."""
    with failures(connection, "Truncate"), engine_of(connection).begin() as cx:
        return cx.execute(delete(entity.__table__)).rowcount


def insert_missing(
    connection: Connection, batches: Sequence[tuple[Any, Sequence[dict[str, Any]]]]
) -> int:
    """Insert every record not already present, in one transaction.

    A record is present when a row equals it in every given Field; a record that
    conflicts with stored data fails the whole insertion and leaves nothing behind.
    """
    inserted = 0
    with (
        failures(connection, "Initial Data insertion"),
        engine_of(connection).begin() as cx,
    ):
        for entity, records in batches:
            table = entity.__table__
            types = {item.name: item.type.value for item in entity.declaration.fields}
            for values in records:
                same = [
                    _expression(table, name, types[name]).is_(None)
                    if value is None
                    else _expression(table, name, types[name]) == value
                    for name, value in values.items()
                ]
                if cx.execute(select(table.c.id).where(*same).limit(1)).first():
                    continue
                try:
                    cx.execute(insert(table).values(**values))
                except IntegrityError:
                    raise ExecutionError(
                        f"Initial Data of {entity.__name__} conflicts with stored data "
                        f"on Instance {connection.instance!r}"
                    ) from None
                inserted += 1
    return inserted
