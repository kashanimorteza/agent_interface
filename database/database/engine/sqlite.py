"""The Engine unit for SQLite: storage behavior behind Core, returning raw results."""

import decimal
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from sqlalchemy import URL, Connection, Engine, event
from sqlalchemy.exc import DBAPIError
from sqlmodel import Session, create_engine

from database.core.configuration import ResolvedInstance
from database.core.errors import (
    ConnectionFailureError,
    DeclarationMismatchError,
    ExecutionError,
)
from database.core.values import (
    CheckedFilter,
    CheckedOrder,
    FilterCombination,
    FilterOperator,
)

EXACT_DECIMAL = "exact_decimal"
EXACT_SUM = "exact_sum"

_ENGINES: dict[Path, Engine] = {}


def _decimal_order(left: str, right: str) -> int:
    first, second = decimal.Decimal(left), decimal.Decimal(right)
    return (first > second) - (first < second)


class _ExactSum:
    """Sums decimal text exactly, ignoring null values."""

    def __init__(self) -> None:
        self.total: decimal.Decimal | None = None

    def step(self, value: Any, /) -> None:
        if value is not None:
            self.total = (self.total or decimal.Decimal(0)) + decimal.Decimal(value)

    def finalize(self) -> Any:
        return None if self.total is None else str(self.total)


def _prepare_connection(foreign_keys: bool) -> Any:
    def prepare(connection: sqlite3.Connection, _: object) -> None:
        connection.isolation_level = None
        if foreign_keys:
            connection.execute("PRAGMA foreign_keys = ON")
        connection.create_collation(EXACT_DECIMAL, _decimal_order)
        connection.create_aggregate(EXACT_SUM, 1, _ExactSum)

    return prepare


def _begin(connection: Connection) -> None:
    connection.exec_driver_sql("BEGIN")


def _engine(instance: ResolvedInstance) -> Engine:
    location = instance.location
    if location is None:
        raise ConnectionFailureError(f"Instance {instance.key!r} has no storage file")
    engine = _ENGINES.get(location)
    if engine is None:
        engine = create_engine(
            URL.create(instance.driver, database=str(location)),
            connect_args=dict(instance.parameters.get("connect_arguments", {})),
        )
        prepare = _prepare_connection(bool(instance.parameters.get("foreign_keys")))
        event.listen(engine, "connect", prepare)
        event.listen(engine, "begin", _begin)
        _ENGINES[location] = engine
    return engine


def _failure(error: DBAPIError) -> str:
    return str(error.orig) if error.orig is not None else type(error).__name__


@contextmanager
def transaction(instance: ResolvedInstance) -> Generator[Session]:
    """One atomic unit of work on the Instance's database file."""
    engine = _engine(instance)
    try:
        if engine.url.database is not None:
            Path(engine.url.database).parent.mkdir(parents=True, exist_ok=True)
        connection = engine.connect()
    except OSError, DBAPIError:
        raise ConnectionFailureError(
            f"cannot connect to Instance {instance.key!r}"
        ) from None
    try:
        with Session(bind=connection) as session, session.begin():
            yield session
    except DBAPIError as error:
        raise ExecutionError(_failure(error)) from None
    finally:
        connection.close()


def _row(session: Session, table: sa.Table, identifier: int) -> dict[str, Any] | None:
    statement: Any = sa.select(table).where(table.c.id == identifier)
    found = session.exec(statement).mappings().first()
    return None if found is None else dict(found)


def _bound(kind: str, value: Any) -> Any:
    return str(value) if kind == "decimal" else value


def _expression(table: sa.Table, name: str, kind: str) -> Any:
    column = table.c[name]
    return column.collate(EXACT_DECIMAL) if kind == "decimal" else column


def _condition(table: sa.Table, checked: CheckedFilter) -> Any:
    column = table.c[checked.field]
    compared = _expression(table, checked.field, checked.type)
    operator, value = checked.operator, checked.value
    if operator is FilterOperator.IS_NULL:
        return column.is_(None)
    if operator is FilterOperator.IS_NOT_NULL:
        return column.is_not(None)
    if operator is FilterOperator.IN:
        return compared.in_([_bound(checked.type, item) for item in value])
    if operator in (
        FilterOperator.CONTAINS,
        FilterOperator.STARTS_WITH,
        FilterOperator.ENDS_WITH,
    ):
        if not value:
            return column.is_not(None)
        if operator is FilterOperator.CONTAINS:
            return sa.func.instr(column, value) > 0
        if operator is FilterOperator.STARTS_WITH:
            return sa.func.substr(column, 1, len(value)) == value
        return sa.func.substr(column, -len(value)) == value
    value = _bound(checked.type, value)
    comparisons = {
        FilterOperator.EQUALS: lambda: compared == value,
        FilterOperator.NOT_EQUALS: lambda: compared.is_distinct_from(value),
        FilterOperator.GREATER_THAN: lambda: compared > value,
        FilterOperator.GREATER_OR_EQUAL: lambda: compared >= value,
        FilterOperator.LESS_THAN: lambda: compared < value,
        FilterOperator.LESS_OR_EQUAL: lambda: compared <= value,
    }
    return comparisons[operator]()


def _where(
    statement: Any,
    table: sa.Table,
    filters: tuple[CheckedFilter, ...],
    combination: FilterCombination,
) -> Any:
    if not filters:
        return statement
    conditions = [_condition(table, checked) for checked in filters]
    combine = sa.and_ if combination is FilterCombination.AND else sa.or_
    return statement.where(combine(*conditions))


def insert(
    instance: ResolvedInstance, entity: Any, values: dict[str, Any]
) -> dict[str, Any] | None:
    """Insert one new record and return its stored row."""
    table = entity.__table__
    with transaction(instance) as session:
        key = session.exec(sa.insert(table).values(values)).inserted_primary_key
        if key is None:
            raise ExecutionError(f"storage assigned no id to the new {entity.__name__}")
        return _row(session, table, key[0])


def update(
    instance: ResolvedInstance, entity: Any, identifier: int, values: dict[str, Any]
) -> dict[str, Any] | None:
    """Replace the given Fields of the record located by its id."""
    table = entity.__table__
    with transaction(instance) as session:
        if _row(session, table, identifier) is None:
            return None
        session.exec(sa.update(table).where(table.c.id == identifier).values(values))
        return _row(session, table, identifier)


def get(
    instance: ResolvedInstance, entity: Any, identifier: int
) -> dict[str, Any] | None:
    """The stored row located by its id."""
    with transaction(instance) as session:
        return _row(session, entity.__table__, identifier)


def select(
    instance: ResolvedInstance,
    entity: Any,
    filters: tuple[CheckedFilter, ...],
    combination: FilterCombination,
    orders: tuple[CheckedOrder, ...],
    limit: int,
) -> list[dict[str, Any]]:
    """The matching rows in the requested order, bounded by a positive limit."""
    table = entity.__table__
    statement = _where(sa.select(table), table, filters, combination)
    for order in orders:
        expression = _expression(table, order.field, order.type)
        statement = statement.order_by(
            expression.desc() if order.descending else expression.asc()
        )
    if limit > 0:
        statement = statement.limit(limit)
    with transaction(instance) as session:
        return [dict(row) for row in session.exec(statement).mappings()]


def delete(
    instance: ResolvedInstance, entity: Any, identifier: int
) -> dict[str, Any] | None:
    """Delete the record located by its id and return its final row."""
    table = entity.__table__
    with transaction(instance) as session:
        row = _row(session, table, identifier)
        if row is not None:
            session.exec(sa.delete(table).where(table.c.id == identifier))
        return row


def truncate(instance: ResolvedInstance, entity: Any) -> int:
    """Delete every record of the Entity, keep its Table, and return the count."""
    table = entity.__table__
    counted: Any = sa.select(sa.func.count()).select_from(table)
    with transaction(instance) as session:
        total = session.exec(counted).scalar_one()
        session.exec(sa.delete(table))
        return total


def set_activity(
    instance: ResolvedInstance, entity: Any, identifier: int, active: bool
) -> dict[str, Any] | None:
    """Set only the Activity Field of the record located by its id."""
    table = entity.__table__
    with transaction(instance) as session:
        if _row(session, table, identifier) is None:
            return None
        session.exec(
            sa.update(table).where(table.c.id == identifier).values(is_active=active)
        )
        return _row(session, table, identifier)


def count(
    instance: ResolvedInstance,
    entity: Any,
    filters: tuple[CheckedFilter, ...],
    combination: FilterCombination,
) -> int:
    """The number of matching records."""
    table = entity.__table__
    statement = _where(
        sa.select(sa.func.count()).select_from(table), table, filters, combination
    )
    with transaction(instance) as session:
        return session.exec(statement).scalar_one()


def aggregate(
    instance: ResolvedInstance,
    entity: Any,
    function: str,
    field: str,
    kind: str,
    filters: tuple[CheckedFilter, ...],
    combination: FilterCombination,
) -> Any:
    """The sum, minimum, or maximum of one Field over matching records, ignoring nulls."""
    table = entity.__table__
    column = table.c[field]
    if function == "sum" and kind == "decimal":
        expression: Any = sa.func.exact_sum(column)
    elif function == "sum":
        expression = sa.func.sum(column, type_=column.type)
    else:
        compared = _expression(table, field, kind)
        chosen = sa.func.min if function == "min" else sa.func.max
        expression = chosen(compared, type_=column.type)
    statement = _where(
        sa.select(expression).select_from(table), table, filters, combination
    )
    with transaction(instance) as session:
        value = session.exec(statement).scalar_one()
    if function == "sum" and kind == "decimal" and value is not None:
        return decimal.Decimal(value)
    return value


def execute(
    instance: ResolvedInstance, command: str, parameters: Any
) -> tuple[list[dict[str, Any]] | None, int | None, list[str] | None]:
    """Run one native SQLite command with bound parameters."""
    bound = tuple(parameters) if isinstance(parameters, list) else parameters
    with transaction(instance) as session:
        result = session.connection().exec_driver_sql(command, bound or ())
        if result.returns_rows:
            columns = list(result.keys())
            return [dict(row) for row in result.mappings()], None, columns
        affected = result.rowcount
        return None, affected if affected >= 0 else None, None


def _shape(columns: Any) -> tuple[str, ...]:
    return tuple(column.name for column in columns)


def _differences(inspector: Any, table: sa.Table, dialect: Any) -> list[str]:
    name = table.name
    stored = {column["name"]: column for column in inspector.get_columns(name)}
    problems: list[str] = []
    if set(stored) != set(table.c.keys()):
        problems.append(f"Table {name!r} has different Fields")
    else:
        for column in table.columns:
            found = stored[column.name]
            if found["nullable"] != column.nullable:
                problems.append(f"Table {name!r} Field {column.name!r} nullability")
            if str(found["type"]).upper() != column.type.compile(dialect).upper():
                problems.append(f"Table {name!r} Field {column.name!r} type")
    primary = tuple(inspector.get_pk_constraint(name)["constrained_columns"])
    if primary != _shape(table.primary_key.columns):
        problems.append(f"Table {name!r} Primary Key")
    stored_relations = {
        (
            tuple(key["constrained_columns"]),
            key["referred_table"],
            tuple(key["referred_columns"]),
        )
        for key in inspector.get_foreign_keys(name)
    }
    relations = {
        (
            _shape(key.columns),
            key.referred_table.name,
            tuple(element.column.name for element in key.elements),
        )
        for key in table.foreign_key_constraints
    }
    if stored_relations != relations:
        problems.append(f"Table {name!r} Relations")
    stored_unique = {
        tuple(entry["column_names"]) for entry in inspector.get_unique_constraints(name)
    }
    unique = {
        _shape(constraint.columns)
        for constraint in table.constraints
        if isinstance(constraint, sa.UniqueConstraint)
    }
    if stored_unique != unique:
        problems.append(f"Table {name!r} Uniqueness Constraints")
    stored_indexes = {
        (tuple(entry["column_names"]), bool(entry["unique"]))
        for entry in inspector.get_indexes(name)
    }
    indexes = {(_shape(index.columns), bool(index.unique)) for index in table.indexes}
    if stored_indexes != indexes:
        problems.append(f"Table {name!r} Indexes")
    return problems


def create_tables(instance: ResolvedInstance, tables: tuple[sa.Table, ...]) -> int:
    """Create every missing Table; stop on any difference with an existing one."""
    with transaction(instance) as session:
        connection = session.connection()
        inspector = sa.inspect(connection)
        existing = set(inspector.get_table_names())
        problems = [
            problem
            for table in tables
            if table.name in existing
            for problem in _differences(inspector, table, connection.dialect)
        ]
        if problems:
            raise DeclarationMismatchError(
                "existing Tables differ from their Declarations: " + "; ".join(problems)
            )
        missing = [table for table in tables if table.name not in existing]
        if missing:
            missing[0].metadata.create_all(connection, tables=missing)
        return len(missing)


def _matching(
    session: Session, table: sa.Table, values: dict[str, Any], names: tuple[str, ...]
) -> list[dict[str, Any]]:
    statement: Any = sa.select(table).where(
        sa.and_(*(table.c[name] == values[name] for name in names))
    )
    return [dict(row) for row in session.exec(statement).mappings()]


def insert_initial_data(
    instance: ResolvedInstance,
    items: list[tuple[Any, int, dict[str, Any], tuple[str, ...], tuple[Any, ...]]],
) -> int:
    """Insert every missing record, skip identical ones, and fail on any conflict."""
    inserted = 0
    with transaction(instance) as session:
        for entity, position, values, given, keys in items:
            table = entity.__table__
            where = f"{entity.__name__} Initial Data record {position}"
            found: list[dict[str, Any]] = []
            for key in keys or (given,):
                found += _matching(session, table, values, key)
            if found:
                if all(row[name] == values[name] for row in found for name in given):
                    continue
                raise ExecutionError(f"{where} conflicts with a stored record")
            try:
                session.exec(sa.insert(table).values(values))
            except DBAPIError as error:
                raise ExecutionError(f"{where}: {_failure(error)}") from None
            inserted += 1
    return inserted
