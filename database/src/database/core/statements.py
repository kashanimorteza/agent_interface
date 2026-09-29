"""Engine-independent statements executed by Instance implementations."""

from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

import sqlalchemy as sa

from database.core.vocabulary import (
    CommandResult,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)

NUMERIC_KINDS = ("integer", "float", "decimal")


class Transaction:
    """Reads and inserts that share one atomic change.

    Attributes:
        connection: Connection inside the open transaction.
        tables: Stored structure by Entity name.
    """

    def __init__(
        self, connection: sa.Connection, tables: Mapping[str, sa.Table]
    ) -> None:
        self.connection = connection
        self.tables = tables

    def find(
        self, entity: Any, values: Mapping[str, Any], fields: Sequence[str]
    ) -> dict[str, Any] | None:
        """Return the first record whose named Fields equal the given values, or None."""
        filters = [Filter(name, FilterOperator.EQUALS, values[name]) for name in fields]
        rows = select(
            self.connection,
            self.tables[entity.declaration.name],
            filters,
            FilterCombination.AND,
            [Order(entity.declaration.primary_key)],
            1,
        )
        return rows[0] if rows else None

    def insert(self, entity: Any, values: dict[str, Any]) -> dict[str, Any]:
        """Insert one record and return it as stored."""
        return insert(self.connection, self.tables[entity.declaration.name], values)


def values_of(entity: Any) -> dict[str, Any]:
    """Return the Field values of an Entity, leaving a pending Auto Increment Field out.

    Args:
        entity (Any): Entity instance.

    Returns:
        (dict): Field name to value.
    """
    values: dict[str, Any] = {}
    for field in entity.declaration.fields:
        value = getattr(entity, field.name)
        pending = (
            value is None
            and field.value_generation is not None
            and field.value_generation.value == "auto_increment"
        )
        if not pending:
            values[field.name] = value
    return values


def insert(
    connection: sa.Connection, table: sa.Table, values: dict[str, Any]
) -> dict[str, Any]:
    """Insert one record and return it as stored."""
    statement = sa.insert(table).values(**values).returning(*table.c)
    return dict(connection.execute(statement).one()._mapping)


def update(
    connection: sa.Connection, table: sa.Table, declaration: Any, values: dict[str, Any]
) -> dict[str, Any] | None:
    """Replace every mutable Field of the record located by its identity."""
    key = declaration.primary_key
    changed = {
        field.name: values[field.name]
        for field in declaration.fields
        if field.name != key and not field.immutable and field.name in values
    }
    statement = (
        sa.update(table)
        .where(table.c[key] == values[key])
        .values(**changed)
        .returning(*table.c)
    )
    row = connection.execute(statement).first()
    return None if row is None else dict(row._mapping)


def get(
    connection: sa.Connection, table: sa.Table, key: str, record_id: Any
) -> dict[str, Any] | None:
    """Return the record with the given identity, or None."""
    row = connection.execute(sa.select(table).where(table.c[key] == record_id)).first()
    return None if row is None else dict(row._mapping)


def select(
    connection: sa.Connection,
    table: sa.Table,
    filters: Sequence[Filter],
    combination: FilterCombination,
    orders: Sequence[Order],
    limit: int,
) -> list[dict[str, Any]]:
    """Return matching records ordered as requested; a limit of zero or less means none."""
    statement = sa.select(table)
    if (condition := _condition(table, filters, combination)) is not None:
        statement = statement.where(condition)
    statement = statement.order_by(*(_order(table, order) for order in orders))
    if limit > 0:
        statement = statement.limit(limit)
    return [dict(row._mapping) for row in connection.execute(statement)]


def delete(
    connection: sa.Connection, table: sa.Table, key: str, record_id: Any
) -> bool:
    """Delete the record with the given identity and report whether one existed."""
    return (
        connection.execute(sa.delete(table).where(table.c[key] == record_id)).rowcount
        > 0
    )


def set_active(
    connection: sa.Connection, table: sa.Table, key: str, record_id: Any, active: bool
) -> dict[str, Any] | None:
    """Set the activity Field of the record with the given identity."""
    statement = (
        sa.update(table)
        .where(table.c[key] == record_id)
        .values(is_active=active)
        .returning(*table.c)
    )
    row = connection.execute(statement).first()
    return None if row is None else dict(row._mapping)


def count(
    connection: sa.Connection,
    table: sa.Table,
    filters: Sequence[Filter],
    combination: FilterCombination,
) -> int:
    """Return the number of matching records."""
    statement = sa.select(sa.func.count()).select_from(table)
    if (condition := _condition(table, filters, combination)) is not None:
        statement = statement.where(condition)
    return connection.execute(statement).scalar_one()


def aggregate(
    connection: sa.Connection,
    table: sa.Table,
    function: str,
    field: Any,
    filters: Sequence[Filter],
    combination: FilterCombination,
) -> Any:
    """Return the total, smallest, or largest non-null value of a Field over matching records."""
    column = table.c[field.name]
    condition = _condition(table, filters, combination)
    if function == "sum":
        return _total(connection, table, field, condition)
    statement = sa.select(getattr(sa.func, function)(column))
    if condition is not None:
        statement = statement.where(condition)
    return connection.execute(statement).scalar_one()


def truncate(connection: sa.Connection, table: sa.Table) -> int:
    """Remove every record of a table and return how many were removed."""
    return connection.execute(sa.delete(table)).rowcount


def execute(
    connection: sa.Connection, command: str, parameters: Mapping[str, Any]
) -> CommandResult:
    """Execute a command with named bound parameters and return its Command Result."""
    result = connection.execute(sa.text(command), dict(parameters))
    if result.returns_rows:
        return CommandResult(rows=[dict(row._mapping) for row in result])
    return CommandResult(affected_count=result.rowcount)


def _total(
    connection: sa.Connection, table: sa.Table, field: Any, condition: Any
) -> Any:
    kind = field.type.value
    if kind not in NUMERIC_KINDS:
        raise TypeError(f"{field.name}: Sum requires a numeric Field")
    column = table.c[field.name]
    statement = sa.select(column).where(column.is_not(None))
    if condition is not None:
        statement = statement.where(condition)
    values = connection.execute(statement).scalars().all()
    if kind == "decimal":
        return sum(values, Decimal(0))
    return sum(values)


def _condition(
    table: sa.Table, filters: Sequence[Filter], combination: FilterCombination
) -> Any:
    clauses = [_clause(table.c[f.field], f) for f in filters]
    if not clauses:
        return None
    return (
        sa.and_(*clauses) if combination is FilterCombination.AND else sa.or_(*clauses)
    )


def _clause(column: sa.Column[Any], filter_: Filter) -> Any:
    value = filter_.value
    match filter_.operator:
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
            if isinstance(value, str) or not isinstance(
                value, Sequence | set | frozenset
            ):
                raise TypeError(f"{filter_.field}: in requires a collection of values")
            return column.in_(list(value))
        case FilterOperator.CONTAINS:
            return column.contains(_text(filter_), autoescape=True)
        case FilterOperator.STARTS_WITH:
            return column.startswith(_text(filter_), autoescape=True)
        case FilterOperator.ENDS_WITH:
            return column.endswith(_text(filter_), autoescape=True)
        case FilterOperator.IS_NULL:
            return column.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return column.is_not(None)


def _text(filter_: Filter) -> str:
    if not isinstance(filter_.value, str):
        raise TypeError(f"{filter_.field}: {filter_.operator} requires a string value")
    return filter_.value


def _order(table: sa.Table, order: Order) -> Any:
    column = table.c[order.field]
    return (
        column.asc() if order.direction is OrderDirection.ASCENDING else column.desc()
    )
