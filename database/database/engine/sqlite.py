"""Engine unit: the implementation of the file-backed SQLite Engine."""

import sqlite3
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Engine,
    and_,
    create_engine,
    delete,
    event,
    func,
    insert,
    inspect,
    or_,
    update,
)
from sqlalchemy.dialects.sqlite import dialect as sqlite_dialect
from sqlalchemy.engine import URL
from sqlalchemy.exc import DBAPIError, OperationalError, SQLAlchemyError
from sqlmodel import Session, select

from ..core.configuration import Connection
from ..core.errors import (
    ConnectionFailureError,
    DatabaseError,
    DeclarationMismatchError,
    ExecutionError,
    SetupError,
)
from ..core.values import (
    CheckedFilter,
    CheckedOrder,
    FilterCombination,
    FilterOperator,
)

STORAGE = "file"
REQUIRED = ("database",)

_DECIMAL_COLLATION = "DECIMAL_TEXT"
_engines: dict[str, Engine] = {}


def _compare_decimal_text(left: str, right: str) -> int:
    first, second = Decimal(left), Decimal(right)
    return (first > second) - (first < second)


def _engine(connection: Connection) -> Engine:
    """Return the engine of an Instance, creating it and its storage directory on first use."""
    location = connection.location
    if location is None:
        raise ConnectionFailureError(
            f"The Instance {connection.instance!r} has no storage location"
        )
    key = str(location)
    if key not in _engines:
        try:
            location.parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            raise ConnectionFailureError(
                f"The storage of the Instance {connection.instance!r} could not be prepared"
            ) from None
        engine = create_engine(
            URL.create("sqlite", database=key),
            connect_args={"check_same_thread": False},
        )

        @event.listens_for(engine, "connect")
        def _prepare_connection(
            dbapi_connection: sqlite3.Connection, _record: Any
        ) -> None:
            dbapi_connection.isolation_level = None
            dbapi_connection.create_collation(_DECIMAL_COLLATION, _compare_decimal_text)
            dbapi_connection.execute("PRAGMA foreign_keys = ON")

        @event.listens_for(engine, "begin")
        def _begin(sql_connection: Any) -> None:
            sql_connection.exec_driver_sql("BEGIN")

        _engines[key] = engine
    return _engines[key]


@contextmanager
def scope(connection: Connection) -> Generator[Session]:
    """Open a connection to an Instance and give one atomic unit of work that commits only when it completes."""
    engine = _engine(connection)
    session = Session(engine)
    session.info["instance"] = connection.instance
    try:
        session.connection()
    except OperationalError, sqlite3.Error:
        session.close()
        raise ConnectionFailureError(
            f"The connection to the Instance {connection.instance!r} could not be opened"
        ) from None
    try:
        yield session
        session.commit()
    except DatabaseError:
        session.rollback()
        raise
    except SQLAlchemyError as error:
        session.rollback()
        detail = getattr(error, "orig", None) if isinstance(error, DBAPIError) else None
        raise ExecutionError(
            f"The request failed on the Instance {connection.instance!r}"
            + (f": {detail}" if detail else "")
        ) from None
    except OverflowError:
        session.rollback()
        raise ExecutionError(
            f"The request carries a value too large for the Instance {connection.instance!r}"
        ) from None
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


def _table(entity: Any) -> Any:
    return entity.__table__


def _row(table: Any, row: Any) -> dict[str, Any]:
    return dict(zip(table.c.keys(), row, strict=True))


def _column(table: Any, name: str, type_name: str) -> Any:
    column = table.c[name]
    return column.collate(_DECIMAL_COLLATION) if type_name == "decimal" else column


def _condition(table: Any, item: CheckedFilter) -> Any:
    column = _column(table, item.field, item.type)
    value = item.value
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
            return func.instr(column, value) > 0
        case FilterOperator.STARTS_WITH:
            return func.substr(column, 1, len(value)) == value
        case FilterOperator.ENDS_WITH:
            return (
                func.substr(column, -len(value)) == value
                if value
                else column.is_not(None)
            )
        case FilterOperator.IS_NULL:
            return column.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return column.is_not(None)


def _where(
    table: Any, filters: Sequence[CheckedFilter], combination: FilterCombination
) -> list[Any]:
    conditions = [_condition(table, item) for item in filters]
    if not conditions:
        return []
    return [
        and_(*conditions) if combination is FilterCombination.AND else or_(*conditions)
    ]


def _primary_key(entity: Any) -> Any:
    return _table(entity).c[entity.declaration.primary_key]


def _fetch(session: Session, entity: Any, identifier: Any) -> dict[str, Any] | None:
    table = _table(entity)
    row = session.exec(
        select(*table.c).where(_primary_key(entity) == identifier)
    ).first()
    return None if row is None else _row(table, row)


def add(session: Session, entity: Any, values: Mapping[str, Any]) -> dict[str, Any]:
    """Store one new record and return the stored row, including generated values."""
    table = _table(entity)
    result = session.exec(insert(table).values(**values))
    key = result.inserted_primary_key
    row = None if key is None else _fetch(session, entity, key[0])
    if row is None:
        raise ExecutionError(f"The new {entity.__name__} record could not be read back")
    return row


def get_by_id(session: Session, entity: Any, identifier: Any) -> dict[str, Any] | None:
    """Return the stored row with an identifier, or None when no such record exists."""
    return _fetch(session, entity, identifier)


def update_row(
    session: Session, entity: Any, identifier: Any, values: Mapping[str, Any]
) -> dict[str, Any] | None:
    """Replace the given mutable values of a record and return the stored row, or None when no record exists."""
    table = _table(entity)
    if _fetch(session, entity, identifier) is None:
        return None
    if values:
        session.exec(
            update(table).where(_primary_key(entity) == identifier).values(**values)
        )
    return _fetch(session, entity, identifier)


def delete_row(session: Session, entity: Any, identifier: Any) -> dict[str, Any] | None:
    """Remove a record and return the row as it was stored, or None when no record exists."""
    row = _fetch(session, entity, identifier)
    if row is None:
        return None
    session.exec(delete(_table(entity)).where(_primary_key(entity) == identifier))
    return row


def set_active(
    session: Session, entity: Any, identifier: Any, active: bool
) -> dict[str, Any] | None:
    """Set only the activity Field of a record and return the final row, or None when no record exists."""
    return update_row(session, entity, identifier, {"is_active": active})


def list_rows(
    session: Session,
    entity: Any,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
    orders: Sequence[CheckedOrder],
    limit: int,
) -> list[dict[str, Any]]:
    """Return the rows that satisfy the Filters, ordered as given and bounded by the limit."""
    table = _table(entity)
    statement = select(*table.c).where(*_where(table, filters, combination))
    for item in orders:
        column = _column(table, item.field, item.type)
        statement = statement.order_by(
            column.desc() if item.descending else column.asc()
        )
    if limit > 0:
        statement = statement.limit(limit)
    return [_row(table, row) for row in session.exec(statement).all()]


def count(
    session: Session,
    entity: Any,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> int:
    """Return the number of rows that satisfy the Filters."""
    table = _table(entity)
    statement = (
        select(func.count())
        .select_from(table)
        .where(*_where(table, filters, combination))
    )
    return int(session.exec(statement).one())


def _values(
    session: Session,
    entity: Any,
    field: str,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> list[Any]:
    table = _table(entity)
    column = table.c[field]
    statement = select(column).where(
        column.is_not(None), *_where(table, filters, combination)
    )
    return list(session.exec(statement).all())


def total(
    session: Session,
    entity: Any,
    field: str,
    type_name: str,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Any:
    """Return the total of a numeric Field over the matching rows, ignoring nulls, or zero when nothing matches."""
    values = _values(session, entity, field, filters, combination)
    if type_name == "decimal":
        return sum(values, Decimal(0))
    return sum(values) if type_name == "integer" else float(sum(values))


def smallest(
    session: Session,
    entity: Any,
    field: str,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Any:
    """Return the smallest non-null value of a Field over the matching rows, or None when nothing matches."""
    values = _values(session, entity, field, filters, combination)
    return min(values) if values else None


def largest(
    session: Session,
    entity: Any,
    field: str,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Any:
    """Return the largest non-null value of a Field over the matching rows, or None when nothing matches."""
    values = _values(session, entity, field, filters, combination)
    return max(values) if values else None


def truncate(session: Session, entity: Any) -> int:
    """Remove every record of an Entity, keeping its Table, and return how many were removed."""
    result = session.exec(delete(_table(entity)))
    return int(result.rowcount)


def execute_command(
    session: Session, command: str, parameters: Mapping[str, Any] | Sequence[Any] | None
) -> tuple[list[dict[str, Any]] | None, int | None, list[str] | None]:
    """Run a native command with bound parameters and return its rows, affected count, and column names."""
    bound = (
        dict(parameters) if isinstance(parameters, Mapping) else tuple(parameters or ())
    )
    result = session.connection().exec_driver_sql(command, bound)
    if result.returns_rows:
        columns = list(result.keys())
        return (
            [dict(zip(columns, row, strict=True)) for row in result.fetchall()],
            None,
            columns,
        )
    return None, max(result.rowcount, 0), None


def _column_differences(
    declaration: Any, table: Any, columns: Mapping[str, Any]
) -> list[str]:
    problems: list[str] = []
    expected = {item.name: item for item in declaration.fields}
    for name in expected.keys() - columns.keys():
        problems.append(f"the column {name} is missing")
    for name in columns.keys() - expected.keys():
        problems.append(f"the column {name} is not in the Declaration")
    dialect = sqlite_dialect()
    for name in expected.keys() & columns.keys():
        if bool(columns[name]["nullable"]) != expected[name].nullable:
            problems.append(f"the column {name} differs in nullability")
        wanted = table.c[name].type.compile(dialect=dialect).upper()
        if str(columns[name]["type"]).upper() != wanted:
            problems.append(f"the column {name} differs in type")
    return problems


def _constraint_differences(
    inspector: Any, entity: Any, physical: Mapping[str, str]
) -> list[str]:
    name, declaration = entity.__name__, entity.declaration
    problems: list[str] = []
    key = inspector.get_pk_constraint(name)["constrained_columns"]
    if list(key) != [declaration.primary_key]:
        problems.append("the Primary Key differs")
    relations = {
        ((item.local_field,), physical[item.target_entity], (item.target_field,))
        for item in declaration.relations
    }
    foreign = {
        (
            tuple(item["constrained_columns"]),
            item["referred_table"],
            tuple(item["referred_columns"]),
        )
        for item in inspector.get_foreign_keys(name)
    }
    if relations != foreign:
        problems.append("the Relations differ")
    indexes = inspector.get_indexes(name)
    unique = {
        tuple(item["column_names"]) for item in inspector.get_unique_constraints(name)
    }
    unique |= {tuple(item["column_names"]) for item in indexes if item["unique"]}
    if unique != {tuple(item.fields) for item in declaration.unique_constraints}:
        problems.append("the Uniqueness Constraints differ")
    plain = {tuple(item["column_names"]) for item in indexes if not item["unique"]}
    if plain != {tuple(item.fields) for item in declaration.indexes}:
        problems.append("the Indexes differ")
    return problems


def create_tables(session: Session, entities: Sequence[Any]) -> tuple[int, int]:
    """Create the Table of every supplied Entity that is missing and return how many were created and how many already matched.

    Every existing Table is compared with its Declaration first; any difference stops the work, is reported,
    and leaves every Table as it was. Creation is one unit of work, so a failure creates no Table.
    """
    connection = session.connection()
    inspector = inspect(connection)
    existing = set(inspector.get_table_names())
    physical = {entity.declaration.name: entity.__name__ for entity in entities}
    differences: list[str] = []
    for entity in entities:
        if entity.__name__ not in existing:
            continue
        found = _column_differences(
            entity.declaration,
            _table(entity),
            {item["name"]: item for item in inspector.get_columns(entity.__name__)},
        ) + _constraint_differences(inspector, entity, physical)
        differences += [f"{entity.__name__}: {problem}" for problem in found]
    if differences:
        raise DeclarationMismatchError(
            "An existing Table differs from its Entity Declaration: "
            + "; ".join(differences)
        )
    missing = [_table(entity) for entity in entities if entity.__name__ not in existing]
    if missing:
        try:
            entities[0].metadata.create_all(
                bind=connection, tables=missing, checkfirst=False
            )
        except SQLAlchemyError:
            raise SetupError(
                f"Table creation did not complete on the Instance {session.info['instance']!r} and no Table was created"
            ) from None
    return len(missing), len(entities) - len(missing)
