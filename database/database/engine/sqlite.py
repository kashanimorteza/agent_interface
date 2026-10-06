"""The Engine unit of the SQLite Engine.

One unit serves every active Instance of this Engine; Instances differ only in the connection Core
passes in. The unit implements storage behaviour and returns raw results: it defines no public
contract and no shared routing.
"""

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import (
    Boolean,
    Integer,
    UniqueConstraint,
    and_,
    delete,
    event,
    func,
    insert,
    inspect,
    or_,
    select,
    type_coerce,
    update,
)
from sqlalchemy import Engine as SqlEngine
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import create_engine

from database.core.configuration import Connection
from database.core.errors import (
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DeclarationMismatchError,
    ExecutionError,
    LifecycleError,
)
from database.core.query import Condition, Sorting
from database.core.values import FilterCombination, FilterOperator


class _Conflict(Exception):
    """An Initial Data record conflicts with a stored one; it carries a public message."""


_NULL_TESTS = (FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL)
_ZERO: dict[str, Any] = {"integer": 0, "float": 0.0, "decimal": Decimal(0)}


def _prepare_connection(dbapi_connection: Any, _record: Any, *, references: bool) -> None:
    # Take over transaction control so that every statement, including schema changes, is atomic.
    dbapi_connection.isolation_level = None
    if references:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def _begin(connection: Any) -> None:
    connection.exec_driver_sql("BEGIN")


def _deferred(condition: Condition) -> bool:
    """A decimal is stored as exact text, so its comparisons are decided on the exact value."""
    return condition.type == "decimal" and condition.operator not in _NULL_TESTS


def _clause(table: Any, condition: Condition) -> ColumnElement[Any]:
    column = table.c[condition.field]
    value = condition.value
    match condition.operator:
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
        case FilterOperator.IS_NULL:
            return column.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return column.is_not(None)
        case FilterOperator.CONTAINS:
            return column.is_not(None) if value == "" else func.instr(column, value) > 0
        case FilterOperator.STARTS_WITH:
            if value == "":
                return column.is_not(None)
            return func.substr(column, 1, len(value)) == value
        case FilterOperator.ENDS_WITH:
            if value == "":
                return column.is_not(None)
            return func.substr(column, -len(value)) == value
    raise ExecutionError("The operator is not supported")


def _test(row: Mapping[str, Any], condition: Condition) -> bool:
    value = row[condition.field]
    operator = condition.operator
    if operator is FilterOperator.IS_NULL:
        return value is None
    if operator is FilterOperator.IS_NOT_NULL:
        return value is not None
    if value is None:
        return False
    other = condition.value
    match operator:
        case FilterOperator.EQUALS:
            return value == other
        case FilterOperator.NOT_EQUALS:
            return value != other
        case FilterOperator.GREATER_THAN:
            return value > other
        case FilterOperator.GREATER_OR_EQUAL:
            return value >= other
        case FilterOperator.LESS_THAN:
            return value < other
        case FilterOperator.LESS_OR_EQUAL:
            return value <= other
        case FilterOperator.IN:
            return any(value == each for each in other)
        case FilterOperator.CONTAINS:
            return other in value
        case FilterOperator.STARTS_WITH:
            return value.startswith(other)
        case FilterOperator.ENDS_WITH:
            return value.endswith(other)
    return False


def _where(
    table: Any, conditions: Sequence[Condition], combination: FilterCombination
) -> ColumnElement[bool] | None:
    clauses = [_clause(table, condition) for condition in conditions]
    if not clauses:
        return None
    return and_(*clauses) if combination is FilterCombination.AND else or_(*clauses)


_VALID = "_valid_"


def _select(table: Any) -> Any:
    """Select every column, plus a validity check for each Boolean column.

    The storage type layer turns any stored value into a boolean, so a stored value that is not
    an integer 0 or 1 would otherwise be repaired silently instead of reported.
    """
    checks = [
        and_(func.typeof(column) == "integer", type_coerce(column, Integer).in_([0, 1])).label(
            f"{_VALID}{column.name}"
        )
        for column in table.columns
        if isinstance(column.type, Boolean)
    ]
    return select(table, *checks)


def _dict(row: Any, table: Any = None) -> dict[str, Any]:
    values = dict(row._mapping)
    for key in [key for key in values if key.startswith(_VALID)]:
        if not values.pop(key):
            where = f" of {table.name}" if table is not None else ""
            raise DeclarationMismatchError(
                f"A stored row{where} has a value that does not match the Type of "
                f"{key.removeprefix(_VALID)}"
            )
    return values


class Engine:
    """Storage behaviour for the Instances that use this Engine."""

    def __init__(self, connection: Connection) -> None:
        self._connection = connection
        self._engine: SqlEngine | None = None

    # ------------------------------------------------------------ storage
    def database_path(self) -> Path:
        """Resolve the Instance's database identity beneath the Database-owned storage root.

        Nothing is created and no connection is made here.
        """
        key = self._connection.instance.key
        identity = Path(self._connection.instance.database)
        root = self._connection.storage_root
        if identity.is_absolute() or ".." in identity.parts or identity.name == "":
            raise ConfigurationError(f"The database of Instance {key} must stay in the storage")
        path = (root / identity).resolve()
        if not path.is_relative_to(root):
            raise ConfigurationError(f"The database of Instance {key} escapes its storage")
        return path

    # ------------------------------------------------------------ connection
    def _connect(self) -> SqlEngine:
        if self._engine is None:
            key = self._connection.instance.key
            path = self.database_path()
            parameters = self._connection.engine.parameters
            references = bool(parameters.get("foreign_keys"))
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                engine = create_engine(
                    URL.create("sqlite", database=str(path)),
                    connect_args=dict(parameters.get("connect_arguments", {})),
                )
                event.listen(
                    engine,
                    "connect",
                    lambda dbapi, record: _prepare_connection(dbapi, record, references=references),
                )
                event.listen(engine, "begin", _begin)
                with engine.connect():
                    pass
            except OSError, SQLAlchemyError:
                raise ConnectionFailureError(f"The Instance {key} could not be reached") from None
            self._engine = engine
        return self._engine

    @contextmanager
    def _transaction(self, entity_cls: Any = None) -> Iterator[Any]:
        """One atomic unit of work: it commits when the block ends and rolls back on any failure."""
        engine = self._connect()
        try:
            with engine.begin() as connection:
                yield connection
        except DatabaseError:
            raise
        except ArithmeticError, ValueError, TypeError:
            # A stored value that cannot become its Field's Type; the value is never shown.
            name = "a stored" if entity_cls is None else f"a stored {entity_cls.declaration.name}"
            raise DeclarationMismatchError(
                f"{name} row has a value that does not match the Type of its Field"
            ) from None
        except SQLAlchemyError:
            raise ExecutionError(
                "The request could not be executed or violates a constraint"
            ) from None

    # ------------------------------------------------------------ reading helpers
    @staticmethod
    def _row(connection: Any, table: Any, key: str, identity: Any) -> dict[str, Any] | None:
        row = connection.execute(_select(table).where(table.c[key] == identity)).first()
        return None if row is None else _dict(row, table)

    @staticmethod
    def _matching(
        connection: Any, table: Any, conditions: Sequence[Condition], combination: FilterCombination
    ) -> list[dict[str, Any]]:
        """Rows matching the conditions; exact-decimal conditions are decided in Python."""
        deferred = [c for c in conditions if _deferred(c)]
        if combination is FilterCombination.AND:
            pushed = [c for c in conditions if not _deferred(c)]
            tested = deferred
        elif deferred:
            pushed, tested = [], list(conditions)
        else:
            pushed, tested = list(conditions), []
        statement = _select(table)
        where = _where(table, pushed, combination)
        if where is not None:
            statement = statement.where(where)
        rows = [_dict(row, table) for row in connection.execute(statement)]
        if not tested:
            return rows
        everything = combination is FilterCombination.AND
        return [
            row
            for row in rows
            if (all if everything else any)(_test(row, condition) for condition in tested)
        ]

    # ------------------------------------------------------------ Entity Operations
    def add(self, entity_cls: Any, values: Mapping[str, Any]) -> dict[str, Any] | None:
        table = entity_cls.__table__
        key = entity_cls.declaration.primary_key
        with self._transaction(entity_cls) as connection:
            result = connection.execute(insert(table).values(**values))
            return self._row(connection, table, key, result.inserted_primary_key[0])

    def update(
        self, entity_cls: Any, identity: Any, values: Mapping[str, Any]
    ) -> dict[str, Any] | None:
        table = entity_cls.__table__
        key = entity_cls.declaration.primary_key
        with self._transaction(entity_cls) as connection:
            if self._row(connection, table, key, identity) is None:
                return None
            if values:
                connection.execute(update(table).where(table.c[key] == identity).values(**values))
            return self._row(connection, table, key, identity)

    def list(
        self,
        entity_cls: Any,
        conditions: Sequence[Condition],
        combination: FilterCombination,
        sortings: Sequence[Sorting],
        limit: int | None,
    ) -> list[dict[str, Any]]:
        table = entity_cls.__table__
        key = entity_cls.declaration.primary_key
        orders = list(sortings)
        if not any(sorting.field == key for sorting in orders):
            orders.append(Sorting(key, "integer", False))  # a stable, repeatable tie-break
        with self._transaction(entity_cls) as connection:
            if any(_deferred(c) for c in conditions) or any(s.type == "decimal" for s in orders):
                rows = self._matching(connection, table, conditions, combination)
                for sorting in reversed(orders):
                    field = sorting.field
                    rows.sort(
                        key=lambda r, f=field: (r[f] is not None, r[f]), reverse=sorting.descending
                    )
                return rows[:limit] if limit else rows
            statement = _select(table)
            where = _where(table, conditions, combination)
            if where is not None:
                statement = statement.where(where)
            statement = statement.order_by(
                *[
                    table.c[s.field].desc() if s.descending else table.c[s.field].asc()
                    for s in orders
                ]
            )
            if limit:
                statement = statement.limit(limit)
            return [_dict(row, table) for row in connection.execute(statement)]

    def get_by_id(self, entity_cls: Any, identity: Any) -> dict[str, Any] | None:
        table = entity_cls.__table__
        with self._transaction(entity_cls) as connection:
            return self._row(connection, table, entity_cls.declaration.primary_key, identity)

    def delete(self, entity_cls: Any, identity: Any) -> dict[str, Any] | None:
        table = entity_cls.__table__
        key = entity_cls.declaration.primary_key
        with self._transaction(entity_cls) as connection:
            row = self._row(connection, table, key, identity)
            if row is not None:
                connection.execute(delete(table).where(table.c[key] == identity))
            return row

    def set_active(self, entity_cls: Any, identity: Any, active: bool) -> dict[str, Any] | None:
        table = entity_cls.__table__
        key = entity_cls.declaration.primary_key
        with self._transaction(entity_cls) as connection:
            if self._row(connection, table, key, identity) is None:
                return None
            connection.execute(
                update(table).where(table.c[key] == identity).values(is_active=active)
            )
            return self._row(connection, table, key, identity)

    def count(
        self, entity_cls: Any, conditions: Sequence[Condition], combination: FilterCombination
    ) -> int:
        table = entity_cls.__table__
        with self._transaction(entity_cls) as connection:
            if any(_deferred(c) for c in conditions):
                return len(self._matching(connection, table, conditions, combination))
            statement = select(func.count()).select_from(table)
            where = _where(table, conditions, combination)
            if where is not None:
                statement = statement.where(where)
            return int(connection.execute(statement).scalar_one())

    def aggregate(
        self,
        entity_cls: Any,
        kind: str,
        field: str,
        type_name: str,
        conditions: Sequence[Condition],
        combination: FilterCombination,
    ) -> Any:
        table = entity_cls.__table__
        with self._transaction(entity_cls) as connection:
            if type_name == "decimal" or any(_deferred(c) for c in conditions):
                rows = self._matching(connection, table, conditions, combination)
                values = [row[field] for row in rows if row[field] is not None]
                if kind == "sum":
                    return sum(values, _ZERO[type_name])
                if not values:
                    return None
                return min(values) if kind == "min" else max(values)
            function = {"sum": func.sum, "min": func.min, "max": func.max}[kind]
            statement = select(function(table.c[field]))
            where = _where(table, conditions, combination)
            if where is not None:
                statement = statement.where(where)
            result = connection.execute(statement).scalar_one()
            if kind == "sum":
                return _ZERO[type_name] if result is None else result
            return result

    def truncate(self, entity_cls: Any) -> int:
        with self._transaction(entity_cls) as connection:
            return int(connection.execute(delete(entity_cls.__table__)).rowcount)

    # ------------------------------------------------------------ native commands
    def execute_command(
        self, command: str, parameters: Mapping[str, Any] | Sequence[Any] | None
    ) -> dict[str, Any]:
        bound: Any = parameters if isinstance(parameters, Mapping) else tuple(parameters or ())
        with self._transaction() as connection:
            result = connection.exec_driver_sql(command, bound)
            if result.returns_rows:
                columns = tuple(result.keys())
                rows = [_dict(row) for row in result]
                return {
                    "rows": rows,
                    "affected": None,
                    "columns": columns,
                    "message": f"Returned {len(rows)} rows",
                }
            affected = max(int(result.rowcount), 0)
            return {
                "rows": None,
                "affected": affected,
                "columns": None,
                "message": f"Affected {affected} rows",
            }

    # ------------------------------------------------------------ Tables
    def create_tables(self, entities: Sequence[Any]) -> dict[str, int]:
        """Create every missing Table from the Entities' table definitions, atomically.

        A Table that already exists is left unchanged. An incomplete creation is a failure.
        """
        with self._transaction() as connection:
            existing = set(self._table_names(connection))
            missing = [
                entity.__table__ for entity in entities if entity.__table__.name not in existing
            ]
            try:
                if missing:
                    missing[0].metadata.create_all(connection, tables=missing, checkfirst=False)
            except SQLAlchemyError:
                raise LifecycleError(
                    "Table creation did not complete; the Instance is left unchanged"
                ) from None
            return {"created": len(missing), "existing": len(entities) - len(missing)}

    @staticmethod
    def _table_names(connection: Any) -> list[str]:
        return list(inspect(connection).get_table_names())

    def differences(self, entities: Sequence[Any]) -> dict[str, list[str]]:
        """Report how each existing Table differs from its Entity's definition; change nothing.

        A Table that does not exist yet is not a difference. Only structure is named, never data.
        """
        found: dict[str, list[str]] = {}
        with self._transaction() as connection:
            inspector = inspect(connection)
            existing = set(inspector.get_table_names())
            for entity in entities:
                table = entity.__table__
                if table.name in existing:
                    problems = self._differences(connection, inspector, table)
                    if problems:
                        found[entity.declaration.name] = problems
        return found

    @staticmethod
    def _differences(connection: Any, inspector: Any, table: Any) -> list[str]:
        name = table.name
        problems: list[str] = []
        reflected = {column["name"]: column for column in inspector.get_columns(name)}
        expected = {column.name: column for column in table.columns}
        problems += [f"column {n} is missing" for n in expected if n not in reflected]
        problems += [f"column {n} is not expected" for n in reflected if n not in expected]
        for column_name in expected.keys() & reflected.keys():
            column, stored = expected[column_name], reflected[column_name]
            if bool(stored["nullable"]) != bool(column.nullable):
                problems.append(f"column {column_name} differs in nullability")
            wanted = column.type.compile(dialect=connection.dialect)
            if str(stored["type"]).upper() != wanted.upper():
                problems.append(f"column {column_name} differs in type")
        stored_keys = set(inspector.get_pk_constraint(name)["constrained_columns"])
        if stored_keys != {column.name for column in table.primary_key.columns}:
            problems.append("the primary key differs")
        stored_links = {
            (tuple(fk["constrained_columns"]), fk["referred_table"], tuple(fk["referred_columns"]))
            for fk in inspector.get_foreign_keys(name)
        }
        wanted_links = {
            (
                tuple(column.name for column in constraint.columns),
                constraint.referred_table.name,
                tuple(element.column.name for element in constraint.elements),
            )
            for constraint in table.foreign_key_constraints
        }
        if stored_links != wanted_links:
            problems.append("the relations differ")
        stored_unique = {
            tuple(unique["column_names"]) for unique in inspector.get_unique_constraints(name)
        }
        wanted_unique = {
            tuple(column.name for column in constraint.columns)
            for constraint in table.constraints
            if isinstance(constraint, UniqueConstraint)
        }
        if stored_unique != wanted_unique:
            problems.append("the uniqueness constraints differ")
        stored_indexes = {
            tuple(index["column_names"])
            for index in inspector.get_indexes(name)
            if not index["unique"]
        }
        wanted_indexes = {
            tuple(column.name for column in index.columns)
            for index in table.indexes
            if not index.unique
        }
        if stored_indexes != wanted_indexes:
            problems.append("the indexes differ")
        return problems

    def insert_initial(self, records: Sequence[tuple[Any, Mapping[str, Any]]]) -> dict[str, Any]:
        """Insert every missing record, in order, atomically.

        A stored record with identical values is skipped. A record that is not identical but takes
        a value that a uniqueness constraint reserves is a conflict, and then nothing is inserted.
        """
        inserted = skipped = 0
        try:
            with self._transaction() as connection:
                for entity_cls, values in records:
                    table = entity_cls.__table__
                    stored = [_dict(row, table) for row in connection.execute(_select(table))]
                    if any(
                        all(row[name] == value for name, value in values.items()) for row in stored
                    ):
                        skipped += 1
                        continue
                    for unique in entity_cls.declaration.unique_constraints:
                        fields = unique.fields
                        if any(values[name] is None for name in fields):
                            continue
                        if any(all(row[name] == values[name] for name in fields) for row in stored):
                            label = entity_cls.declaration.name
                            where = ", ".join(fields)
                            raise _Conflict(
                                f"a {label} record conflicts with a stored one on {where}"
                            )
                    connection.execute(insert(table).values(**values))
                    inserted += 1
        except _Conflict as conflict:
            return {"inserted": 0, "skipped": 0, "conflict": str(conflict)}
        return {"inserted": inserted, "skipped": skipped, "conflict": None}
