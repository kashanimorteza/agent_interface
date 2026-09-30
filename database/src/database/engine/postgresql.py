"""The server-based Instance: a complete implementation over a database server.

It implements every Entity Operation, ExecuteCommand, and the capabilities both
Lifecycle Commands need, and holds everything specific to this Instance: building the
connection from its complete definition, exact fixed-scale decimals, 64-bit integers,
and byte-order ("C" collation) text comparison so ordering does not depend on the
server's locale, and null sorted as the smallest value.
"""

import builtins
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, cast

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Connection,
    DateTime,
    Dialect,
    Float,
    Index,
    Numeric,
    String,
    Table,
    and_,
    create_engine,
    delete,
    func,
    insert,
    inspect,
    or_,
    select,
    text,
    update,
)
from sqlalchemy import (
    Engine as SqlEngine,
)
from sqlalchemy import exc as sa_exc
from sqlalchemy.engine import URL
from sqlalchemy.schema import SchemaItem
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.types import TypeDecorator, TypeEngine

from database.core._config import Configuration, EngineConfig, InstanceConfig
from database.core._contracts import (
    NULL_TESTING,
    Filter,
    FilterCombination,
    FilterOperator,
    OrderDirection,
    Query,
)
from database.core._engine import Record
from database.core._failures import (
    ConnectionFailure,
    DatabaseError,
    DeclarationFailure,
    ExecutionFailure,
)
from database.core._schema import Schema, build_schema

DECIMAL_SCALE = 12
DECIMAL_DIGITS = 38


def _reason(error: BaseException) -> str:
    """One short, value-free line describing a driver failure."""
    original = getattr(error, "orig", error)
    line = str(original).strip().splitlines()
    name = type(original).__name__
    return f"{name}: {line[0][:160]}" if line else name


def _checked(value: Any) -> Decimal:
    """A decimal this Component can hold without altering it, or a refusal."""
    number = Decimal(value)
    if not number.is_finite():
        raise ExecutionFailure("A decimal Field holds only finite values.")
    _, digits, exponent = number.normalize().as_tuple()
    if not isinstance(exponent, int):
        raise ExecutionFailure("A decimal Field holds only finite values.")
    if (
        exponent < -DECIMAL_SCALE
        or len(digits) + exponent > DECIMAL_DIGITS - DECIMAL_SCALE
    ):
        raise ExecutionFailure(
            "A decimal value exceeds the supported precision and would be altered."
        )
    return number


class UtcDateTime(TypeDecorator[datetime]):
    """A time zone aware instant, stored and returned in UTC."""

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise DeclarationFailure(
                "A datetime Field holds only time zone aware values."
            )
        return value.astimezone(UTC)

    def process_result_value(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)


class FixedDecimal(TypeDecorator[Decimal]):
    """A fixed-scale exact decimal; a value that would be altered is refused."""

    impl = Numeric(DECIMAL_DIGITS, DECIMAL_SCALE, asdecimal=True)
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Dialect) -> Decimal | None:
        return None if value is None else _checked(value)


def _column_type(declared: Any) -> TypeEngine[Any]:
    kind: str = declared.type
    size = declared.constraints.get("size")
    if kind == "integer":
        return BigInteger()
    if kind == "string":
        return String(size, collation="C") if size else String(collation="C")
    if kind == "boolean":
        return Boolean()
    if kind == "float":
        return Float()
    if kind == "decimal":
        return FixedDecimal()
    if kind == "datetime":
        return UtcDateTime()
    raise DeclarationFailure(f"Field {declared.name} has an unsupported type.")


_REQUIRED = ("host", "port", "database", "username")


def build_url(instance: InstanceConfig) -> URL:
    """The connection URL of this Instance; every required value must be present."""
    missing = [part for part in _REQUIRED if getattr(instance, part) in (None, "")]
    if instance.password is None:
        missing.append("password")
    if missing:
        raise ConnectionFailure(
            f"Instance {instance.key} lacks required connection values: "
            f"{', '.join(missing)}."
        )
    return URL.create(
        "postgresql+psycopg",
        username=instance.username,
        password=instance.password,
        host=instance.host,
        port=instance.port,
        database=instance.database,
    )


class PostgresqlEngine:
    """The complete implementation of the server-based Instance."""

    def __init__(
        self,
        configuration: Configuration,
        engine: EngineConfig,
        instance: InstanceConfig,
        declarations: Mapping[str, Any],
    ) -> None:
        arguments: dict[str, Any] = {"connect_timeout": 5, **instance.options}
        self._engine: SqlEngine = create_engine(
            build_url(instance), connect_args=arguments
        )
        self._schema: Schema = build_schema(declarations, _column_type)

    # ------------------------------------------------------------ transactions
    @contextmanager
    def _transaction(self) -> Generator[Connection]:
        try:
            connection = self._engine.connect()
        except sa_exc.SQLAlchemyError as error:
            raise ConnectionFailure(
                f"The Instance could not be reached ({_reason(error)})."
            ) from None
        try:
            with connection.begin():
                yield connection
        except DatabaseError:
            raise
        except sa_exc.StatementError as error:
            if isinstance(error.orig, DatabaseError):
                raise error.orig from None
            if isinstance(error, sa_exc.IntegrityError):
                raise ExecutionFailure(
                    "The change violates a Relation or a Uniqueness Constraint."
                ) from None
            kind = type(getattr(error, "orig", error)).__name__
            raise ExecutionFailure(
                f"The Instance failed to execute the request ({kind})."
            ) from None
        except sa_exc.SQLAlchemyError as error:
            kind = type(getattr(error, "orig", error)).__name__
            raise ExecutionFailure(
                f"The Instance failed to execute the request ({kind})."
            ) from None
        except OverflowError:
            raise ExecutionFailure(
                "A value is outside the range the Instance can store."
            ) from None
        finally:
            connection.close()

    # -------------------------------------------------------------- conditions
    def _text_condition(
        self, column: Any, operator: FilterOperator, value: str
    ) -> ColumnElement[bool]:
        if operator is FilterOperator.CONTAINS:
            return column.contains(value, autoescape=True)
        if operator is FilterOperator.STARTS_WITH:
            return column.startswith(value, autoescape=True)
        return column.endswith(value, autoescape=True)

    def _condition(
        self, entity: str, filters: Sequence[Filter], combination: FilterCombination
    ) -> ColumnElement[bool] | None:
        parts: list[ColumnElement[bool]] = []
        for item in filters:
            column = self._schema.column(entity, item.field)
            operator = item.operator
            value = item.value
            if operator is FilterOperator.EQUALS:
                parts.append(column == value)
            elif operator is FilterOperator.NOT_EQUALS:
                parts.append(column != value)
            elif operator is FilterOperator.GREATER_THAN:
                parts.append(column > value)
            elif operator is FilterOperator.GREATER_OR_EQUAL:
                parts.append(column >= value)
            elif operator is FilterOperator.LESS_THAN:
                parts.append(column < value)
            elif operator is FilterOperator.LESS_OR_EQUAL:
                parts.append(column <= value)
            elif operator is FilterOperator.IN:
                parts.append(column.in_(value))
            elif operator in (
                FilterOperator.CONTAINS,
                FilterOperator.STARTS_WITH,
                FilterOperator.ENDS_WITH,
            ):
                parts.append(self._text_condition(column, operator, value))
            elif operator is FilterOperator.IS_NULL:
                parts.append(column.is_(None))
            elif operator in NULL_TESTING:
                parts.append(column.is_not(None))
        if not parts:
            return None
        return and_(*parts) if combination is FilterCombination.AND else or_(*parts)

    def _order(self, column: Any, direction: OrderDirection) -> ColumnElement[Any]:
        # Null sorts as the smallest value, as on every Instance.
        if direction is OrderDirection.ASCENDING:
            return column.asc().nulls_first()
        return column.desc().nulls_last()

    def _record(self, row: Any) -> Record:
        return dict(row._mapping)

    # ---------------------------------------------------------- Entity Operations
    def add(self, entity: str, values: Mapping[str, Any]) -> Record:
        table = self._schema.tables[entity]
        with self._transaction() as connection:
            row = connection.execute(
                insert(table).values(**values).returning(*table.c)
            ).one()
            return self._record(row)

    def update(
        self, entity: str, identifier: int, values: Mapping[str, Any]
    ) -> Record | None:
        table = self._schema.tables[entity]
        with self._transaction() as connection:
            row = connection.execute(
                update(table)
                .where(table.c.id == identifier)
                .values(**values)
                .returning(*table.c)
            ).first()
            return None if row is None else self._record(row)

    def get_by_id(self, entity: str, identifier: int) -> Record | None:
        table = self._schema.tables[entity]
        with self._transaction() as connection:
            row = connection.execute(
                select(table).where(table.c.id == identifier)
            ).first()
            return None if row is None else self._record(row)

    def delete(self, entity: str, identifier: int) -> Record | None:
        table = self._schema.tables[entity]
        with self._transaction() as connection:
            row = connection.execute(
                delete(table).where(table.c.id == identifier).returning(*table.c)
            ).first()
            return None if row is None else self._record(row)

    def enable(self, entity: str, identifier: int) -> Record | None:
        return self.update(entity, identifier, {"is_active": True})

    def disable(self, entity: str, identifier: int) -> Record | None:
        return self.update(entity, identifier, {"is_active": False})

    def list(self, entity: str, query: Query) -> builtins.list[Record]:
        table = self._schema.tables[entity]
        statement = select(table)
        condition = self._condition(entity, query.filters, query.combination)
        if condition is not None:
            statement = statement.where(condition)
        ordering: builtins.list[ColumnElement[Any]] = [
            self._order(table.c[order.field], order.direction) for order in query.orders
        ]
        ordering.append(table.c.id.asc())
        statement = statement.order_by(*ordering)
        if query.limit > 0:
            statement = statement.limit(query.limit)
        with self._transaction() as connection:
            return [self._record(row) for row in connection.execute(statement)]

    def count(self, entity: str, query: Query) -> int:
        table = self._schema.tables[entity]
        statement = select(func.count()).select_from(table)
        condition = self._condition(entity, query.filters, query.combination)
        if condition is not None:
            statement = statement.where(condition)
        with self._transaction() as connection:
            return int(connection.execute(statement).scalar_one())

    def _aggregate(self, entity: str, function: Any, field: str, query: Query) -> Any:
        table = self._schema.tables[entity]
        statement = select(function(table.c[field])).select_from(table)
        condition = self._condition(entity, query.filters, query.combination)
        if condition is not None:
            statement = statement.where(condition)
        with self._transaction() as connection:
            return connection.execute(statement).scalar_one()

    def sum(self, entity: str, field: str, query: Query) -> Any:
        return self._aggregate(entity, func.sum, field, query)

    def min(self, entity: str, field: str, query: Query) -> Any:
        return self._aggregate(entity, func.min, field, query)

    def max(self, entity: str, field: str, query: Query) -> Any:
        return self._aggregate(entity, func.max, field, query)

    def truncate(self, entity: str) -> int:
        table = self._schema.tables[entity]
        with self._transaction() as connection:
            return int(connection.execute(delete(table)).rowcount)

    # ------------------------------------------------------ Database-wide Operation
    def execute_command(
        self, command: str, parameters: Mapping[str, Any]
    ) -> tuple[builtins.list[Record] | None, int | None, builtins.list[str] | None]:
        with self._transaction() as connection:
            result = connection.execute(text(command), dict(parameters))
            if result.returns_rows:
                columns = [str(name) for name in result.keys()]
                return [self._record(row) for row in result], None, columns
            return None, int(result.rowcount), None

    # ---------------------------------------------------------- Lifecycle capabilities
    def create_tables(self) -> int:
        """Create or align every table; only additive change is applied."""
        schema = self._schema
        owned = set(schema.metadata.tables)

        def include(
            item: SchemaItem,
            name: str | None,
            kind: str,
            reflected: bool,
            compare_to: Any,
        ) -> bool:
            return name in owned if kind == "table" else True

        with self._transaction() as connection:
            context = MigrationContext.configure(
                connection,
                opts={
                    "compare_type": False,
                    "compare_server_default": False,
                    "include_object": include,
                },
            )
            operations = Operations(context)
            added_tables: builtins.list[Table] = []
            added_columns: builtins.list[tuple[str, Column[Any]]] = []
            added_indexes: builtins.list[Index] = []
            unsafe: builtins.list[str] = []
            for diff in _flatten(compare_metadata(context, schema.metadata)):
                kind = diff[0]
                if kind == "add_table":
                    added_tables.append(diff[1])
                elif kind == "add_column":
                    column: Column[Any] = diff[3]
                    if column.nullable or column.server_default is not None:
                        added_columns.append((diff[2], column))
                    else:
                        unsafe.append(
                            f"add_column {diff[2]}.{column.name} (not null, no default)"
                        )
                elif kind == "add_index":
                    added_indexes.append(diff[1])
                else:
                    target = (
                        diff[1]
                        if isinstance(diff[1], str)
                        else getattr(diff[1], "name", "")
                    )
                    unsafe.append(f"{kind} {target}".strip())
            if unsafe:
                raise DeclarationFailure(
                    "The stored structure differs from the Declarations in a way "
                    "that cannot be applied safely: "
                    f"{', '.join(sorted(set(unsafe)))}."
                )
            if added_tables:
                schema.metadata.create_all(
                    connection, tables=added_tables, checkfirst=True
                )
            for table_name, column in added_columns:
                operations.add_column(table_name, column.copy())
            for index in added_indexes:
                if index.table is None:
                    continue
                operations.create_index(
                    index.name,
                    index.table.name,
                    [column.name for column in index.columns],
                    unique=index.unique,
                )
            return len(schema.tables)

    def missing_tables(self) -> builtins.list[str]:
        with self._transaction() as connection:
            existing = set(inspect(connection).get_table_names())
        return sorted(
            table.name
            for table in self._schema.tables.values()
            if table.name not in existing
        )

    def insert_missing(self, records: Sequence[tuple[str, Mapping[str, Any]]]) -> int:
        inserted = 0
        with self._transaction() as connection:
            for entity, values in records:
                if self._present(connection, entity, values):
                    continue
                connection.execute(insert(self._schema.tables[entity]).values(**values))
                inserted += 1
        return inserted

    def _present(
        self, connection: Connection, entity: str, values: Mapping[str, Any]
    ) -> bool:
        """Whether an identical record exists; a conflicting record is a failure."""
        table = self._schema.tables[entity]
        declaration = self._schema.declarations[entity]
        for group in declaration.unique_constraints:
            if any(values.get(name) is None for name in group):
                continue
            match = connection.execute(
                select(table).where(
                    and_(*[cast(Any, table.c[name] == values[name]) for name in group])
                )
            ).first()
            if match is None:
                continue
            stored = self._record(match)
            if all(stored[name] == value for name, value in values.items()):
                return True
            raise ExecutionFailure(
                f"Initial Data conflicts with an existing {declaration.name} record."
            )
        conditions = [
            table.c[name].is_(None) if value is None else table.c[name] == value
            for name, value in values.items()
        ]
        found = connection.execute(
            select(table.c.id).where(and_(*conditions)).limit(1)
        ).first()
        return found is not None


def _flatten(diffs: builtins.list[Any]) -> builtins.list[tuple[Any, ...]]:
    flat: builtins.list[tuple[Any, ...]] = []
    for diff in diffs:
        if isinstance(diff, builtins.list):
            flat.extend(_flatten(cast(builtins.list[Any], diff)))
        else:
            flat.append(diff)
    return flat


def create(
    configuration: Configuration,
    engine: EngineConfig,
    instance: InstanceConfig,
    declarations: Mapping[str, Any],
) -> PostgresqlEngine:
    """Build this Instance's implementation from its complete definition."""
    return PostgresqlEngine(configuration, engine, instance, declarations)
