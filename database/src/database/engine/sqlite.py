"""The SQLite Engine unit: storage behaviour for every Instance that uses SQLite."""

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from decimal import localcontext
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, and_, create_engine, event, func, inspect, or_
from sqlalchemy.dialects import sqlite as sqlite_dialect
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.pool import NullPool
from sqlmodel import Session, SQLModel, delete, select

from database.core.data import Connection, Query, fields_of, physical_name
from database.interface import (
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    OrderDirection,
)


def _location(connection: Connection) -> Path:
    """Resolve the Instance's database file beneath Database-owned storage, refusing any location outside it."""
    for name in connection.parameters["required_parameters"]:
        if not getattr(connection, name):
            raise ConfigurationError(
                f"Instance {connection.name!r} needs a value for {name}."
            )
    root = connection.storage_root.resolve()
    path = (root / connection.database).resolve()
    if path == root or not path.is_relative_to(root):
        raise ConfigurationError(
            f"The database of Instance {connection.name!r} must stay inside Database-owned storage."
        )
    return path


def _engine(connection: Connection) -> Engine:
    path = _location(connection)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        raise ConnectionFailureError(
            f"Instance {connection.name!r} cannot be reached: its storage cannot be created."
        ) from None
    engine = create_engine(
        URL.create(connection.parameters["url_scheme"], database=str(path)),
        connect_args=dict(connection.parameters["connect_arguments"]),
        poolclass=NullPool,
    )
    foreign_keys = connection.parameters["foreign_keys"]

    @event.listens_for(engine, "connect")
    def _on_connect(dbapi_connection: Any, _record: Any) -> None:
        dbapi_connection.isolation_level = None
        if foreign_keys:
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    @event.listens_for(engine, "begin")
    def _on_begin(sql_connection: Any) -> None:
        sql_connection.exec_driver_sql("BEGIN")

    return engine


@contextmanager
def _session(connection: Connection, action: str) -> Iterator[Session]:
    """Open one atomic unit of work on the Instance: it commits in full or leaves no change."""
    engine = _engine(connection)
    try:
        try:
            engine.connect().close()
        except OperationalError:
            raise ConnectionFailureError(
                f"Instance {connection.name!r} cannot be reached."
            ) from None
        try:
            with Session(engine) as session:
                yield session
                session.commit()
        except DatabaseError:
            raise
        except SQLAlchemyError as error:
            reason = getattr(error, "orig", None) or type(error).__name__
            raise ExecutionError(
                f"{action} failed on Instance {connection.name!r}: {reason}."
            ) from None
    finally:
        engine.dispose()


def _row(stored: Any) -> dict[str, Any]:
    return {name: getattr(stored, name) for name in type(stored).model_fields}


def add(connection: Connection, entity: Any) -> dict[str, Any]:
    """Store one new Entity and return the stored row, including values the storage generated."""
    with _session(connection, "Add") as session:
        stored = type(entity)(**entity.model_dump())
        session.add(stored)
        session.flush()
        session.refresh(stored)
        return _row(stored)


def _identity(entity: type[Any]) -> str:
    return physical_name(entity, entity.declaration.primary_key)


def update(connection: Connection, entity: Any) -> dict[str, Any] | None:
    """Replace every mutable Field of the record the Entity's identity locates."""
    kind = type(entity)
    with _session(connection, "Update") as session:
        identity = getattr(entity, _identity(kind))
        stored = None if identity is None else session.get(kind, identity)
        if stored is None:
            return None
        for name, declared in fields_of(kind).items():
            if not declared.immutable:
                setattr(stored, name, getattr(entity, name))
        session.flush()
        session.refresh(stored)
        return _row(stored)


def delete_record(
    connection: Connection, entity: type[Any], identity: Any
) -> dict[str, Any] | None:
    """Remove the record an identity locates and return it as it was."""
    with _session(connection, "Delete") as session:
        stored = session.get(entity, identity)
        if stored is None:
            return None
        removed = _row(stored)
        session.delete(stored)
        session.flush()
        return removed


def set_active(
    connection: Connection, entity: type[Any], identity: Any, active: bool
) -> dict[str, Any] | None:
    """Set only the active state of the record an identity locates and return the final record."""
    with _session(connection, "Enable" if active else "Disable") as session:
        stored = session.get(entity, identity)
        if stored is None:
            return None
        stored.is_active = active
        session.flush()
        session.refresh(stored)
        return _row(stored)


def truncate(connection: Connection, entity: type[Any]) -> int:
    """Remove every record of one Entity, keep its Table, and return how many were removed."""
    with _session(connection, "Truncate") as session:
        return session.exec(delete(entity)).rowcount  # pyright: ignore[reportAttributeAccessIssue]


def _is_decimal(entity: type[Any], reference: Any) -> bool:
    return fields_of(entity)[reference.key].type == "decimal"


def _condition(condition: Filter) -> Any:
    field, value = condition.field, condition.value
    match condition.operator:
        case FilterOperator.EQUALS:
            return field == value
        case FilterOperator.NOT_EQUALS:
            return field != value
        case FilterOperator.GREATER_THAN:
            return field > value
        case FilterOperator.GREATER_OR_EQUAL:
            return field >= value
        case FilterOperator.LESS_THAN:
            return field < value
        case FilterOperator.LESS_OR_EQUAL:
            return field <= value
        case FilterOperator.IN:
            return field.in_(value)
        case FilterOperator.CONTAINS:
            return func.instr(field, value) > 0 if value else field.is_not(None)
        case FilterOperator.STARTS_WITH:
            return (
                func.substr(field, 1, len(value)) == value
                if value
                else field.is_not(None)
            )
        case FilterOperator.ENDS_WITH:
            return (
                func.substr(field, -len(value)) == value
                if value
                else field.is_not(None)
            )
        case FilterOperator.IS_NULL:
            return field.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return field.is_not(None)


def _satisfies(stored: Any, condition: Filter) -> bool:
    value, operand = getattr(stored, condition.field.key), condition.value
    match condition.operator:
        case FilterOperator.IS_NULL:
            return value is None
        case FilterOperator.IS_NOT_NULL:
            return value is not None
    if value is None:
        return False
    match condition.operator:
        case FilterOperator.EQUALS:
            return value == operand
        case FilterOperator.NOT_EQUALS:
            return value != operand
        case FilterOperator.GREATER_THAN:
            return value > operand
        case FilterOperator.GREATER_OR_EQUAL:
            return value >= operand
        case FilterOperator.LESS_THAN:
            return value < operand
        case FilterOperator.LESS_OR_EQUAL:
            return value <= operand
        case FilterOperator.IN:
            return value in operand
        case FilterOperator.CONTAINS:
            return operand in value
        case FilterOperator.STARTS_WITH:
            return value.startswith(operand)
        case FilterOperator.ENDS_WITH:
            return value.endswith(operand)
    return False


def _exact(entity: type[Any], query: Query) -> bool:
    """Whether the query touches a Decimal Field, whose exact text storage cannot be compared numerically in SQL."""
    return any(
        _is_decimal(entity, item.field) for item in (*query.filters, *query.orders)
    )


def _where(query: Query) -> Any:
    conditions = [_condition(item) for item in query.filters]
    if not conditions:
        return None
    return (
        and_(*conditions)
        if query.combination is FilterCombination.AND
        else or_(*conditions)
    )


def _matching(session: Session, entity: type[Any], query: Query) -> list[Any]:
    """Return the records a query selects, ordered and limited, with Decimal Fields compared by value."""
    if not _exact(entity, query):
        statement = select(entity)
        where = _where(query)
        if where is not None:
            statement = statement.where(where)
        for order in query.orders:
            statement = statement.order_by(
                order.field.asc()
                if order.direction is OrderDirection.ASCENDING
                else order.field.desc()
            )
        if query.limit > 0:
            statement = statement.limit(query.limit)
        return list(session.exec(statement).all())
    combine = all if query.combination is FilterCombination.AND else any
    records = [
        stored
        for stored in session.exec(select(entity)).all()
        if not query.filters
        or combine(_satisfies(stored, item) for item in query.filters)
    ]
    for order in reversed(query.orders):
        key = order.field.key
        records.sort(
            key=lambda stored, key=key: (
                getattr(stored, key) is not None,
                getattr(stored, key),
            ),
            reverse=order.direction is OrderDirection.DESCENDING,
        )
    return records[: query.limit] if query.limit > 0 else records


def list_records(
    connection: Connection, entity: type[Any], query: Query
) -> list[dict[str, Any]]:
    """Return the records of one Entity that match the query, in the requested order and quantity."""
    with _session(connection, "List") as session:
        return [_row(stored) for stored in _matching(session, entity, query)]


def get(
    connection: Connection, entity: type[Any], identity: Any
) -> dict[str, Any] | None:
    """Return the record an identity locates, or None when none exists."""
    with _session(connection, "Get") as session:
        stored = session.get(entity, identity)
        return None if stored is None else _row(stored)


def execute(connection: Connection, command: str, parameters: Any) -> dict[str, Any]:
    """Run a native command with bound parameters and report its raw outcome."""
    with _session(connection, "Command") as session:
        try:
            bound = (
                tuple(parameters)
                if isinstance(parameters, list | tuple)
                else parameters
            )
            result = session.connection().exec_driver_sql(command, bound or ())
            if result.returns_rows:
                rows = [dict(row._mapping) for row in result]
                return {
                    "rows": rows,
                    "affected": None,
                    "columns": list(result.keys()),
                    "success": True,
                    "message": f"The command returned {len(rows)} row(s).",
                }
            affected = result.rowcount if result.rowcount >= 0 else None
            return {
                "rows": None,
                "affected": affected,
                "columns": None,
                "success": True,
                "message": "The command completed.",
            }
        except SQLAlchemyError as error:
            session.rollback()
            reason = getattr(error, "orig", None) or type(error).__name__
            return {
                "rows": None,
                "affected": None,
                "columns": None,
                "success": False,
                "message": f"The command failed: {reason}.",
            }


def create_tables(connection: Connection, entities: tuple[type[Any], ...]) -> None:
    """Create the Table of every supplied Entity that does not exist yet, leaving existing Tables unchanged."""
    with _session(connection, "CreateTables") as session:
        SQLModel.metadata.create_all(
            session.connection(), tables=[entity.__table__ for entity in entities]
        )


def storage_types(_connection: Connection, entity: type[Any]) -> dict[str, str]:
    """Return the storage type this Engine gives each Field of an Entity."""
    dialect = sqlite_dialect.dialect()
    return {
        column.name: column.type.compile(dialect=dialect)
        for column in entity.__table__.columns
    }


def describe_table(connection: Connection, entity: type[Any]) -> dict[str, Any] | None:
    """Report the stored structure of an Entity's Table, or None when the Table does not exist."""
    name = entity.__table__.name
    with _session(connection, "Describe") as session:
        inspector = inspect(session.connection())
        if not inspector.has_table(name):
            return None
        dialect = sqlite_dialect.dialect()
        return {
            "fields": {
                column["name"]: (
                    column["type"].compile(dialect=dialect),
                    column["nullable"],
                )
                for column in inspector.get_columns(name)
            },
            "primary_key": tuple(
                inspector.get_pk_constraint(name)["constrained_columns"]
            ),
            "relations": frozenset(
                (
                    tuple(key["constrained_columns"]),
                    key["referred_table"],
                    tuple(key["referred_columns"]),
                )
                for key in inspector.get_foreign_keys(name)
            ),
            "unique_constraints": frozenset(
                frozenset(item["column_names"])
                for item in inspector.get_unique_constraints(name)
            ),
            "indexes": frozenset(
                frozenset(item["column_names"]) for item in inspector.get_indexes(name)
            ),
        }


def count(connection: Connection, entity: type[Any], query: Query) -> int:
    """Return how many records of one Entity satisfy the query's Filters."""
    with _session(connection, "Count") as session:
        if _exact(entity, query):
            return len(_matching(session, entity, query))
        statement = select(func.count()).select_from(entity)
        where = _where(query)
        if where is not None:
            statement = statement.where(where)
        return session.exec(statement).one()


def aggregate(
    connection: Connection, entity: type[Any], function: str, field: str, query: Query
) -> Any:
    """Return the total, smallest, or largest non-null value of a Field over the matching records, or None when none match."""
    with _session(connection, "Aggregate") as session:
        if fields_of(entity)[field].type == "decimal" or _exact(entity, query):
            values = [
                value
                for stored in _matching(session, entity, query)
                if (value := getattr(stored, field)) is not None
            ]
            if not values:
                return None
            with localcontext(prec=1000):
                return {"sum": sum, "min": min, "max": max}[function](values)
        statement = select(getattr(func, function)(getattr(entity, field)))
        where = _where(query)
        if where is not None:
            statement = statement.where(where)
        return session.exec(statement).one()


def insert_many(connection: Connection, entities: Sequence[Any]) -> int:
    """Insert an ordered set of Entities as one change: every record is stored in order, or none is."""
    with _session(connection, "Insert") as session:
        for entity in entities:
            session.add(type(entity)(**entity.model_dump()))
            session.flush()
        return len(entities)
