"""SQLite Engine unit: storage behaviour for every Instance that uses the SQLite Engine."""

from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Final, cast

from sqlalchemy import (
    ColumnElement,
    Connection,
    Engine,
    Inspector,
    and_,
    delete,
    event,
    func,
    insert,
    inspect,
    or_,
    text,
    update as sql_update,
)
from sqlalchemy.engine import URL
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlmodel import SQLModel, create_engine, select

from database.core.data import (
    ConnectionFailureError,
    DeclarationMismatchError,
    EngineSpec,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InstanceSpec,
    Order,
    OrderDirection,
    declaration_of,
    table_of,
)

ATOMIC_STRUCTURE_CHANGES: Final = True
_DECIMAL_OFFSET: Final = 10**7


def connect(
    instance: InstanceSpec, engine: EngineSpec, location: Path | None
) -> Engine:
    """Build the connection of one Instance when a request first needs it, and prove it is usable."""
    if location is None:
        raise ConnectionFailureError(
            f"Instance '{instance.key}' has no storage location."
        )
    parameters = engine.parameters
    try:
        location.parent.mkdir(parents=True, exist_ok=True)
        connection = create_engine(
            URL.create(parameters["url_scheme"], database=str(location)),
            connect_args=dict(parameters.get("connect_arguments", {})),
        )
        event.listen(
            connection,
            "connect",
            _prepare_connection(bool(parameters.get("foreign_keys"))),
        )
        event.listen(connection, "begin", _begin_explicitly)
        with connection.connect() as probe:
            probe.execute(text("SELECT 1"))
    except OSError, SQLAlchemyError:
        raise ConnectionFailureError(
            f"Instance '{instance.key}' could not be connected."
        ) from None
    return connection


def _prepare_connection(enforce_relations: bool) -> Any:
    def prepare(dbapi_connection: Any, _record: object) -> None:
        # Explicit transaction control makes structure changes transactional, so a failed change leaves nothing behind.
        dbapi_connection.isolation_level = None
        dbapi_connection.create_function(
            "decimal_key", 1, _decimal_key, deterministic=True
        )
        if enforce_relations:
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("PRAGMA foreign_keys=ON")
            finally:
                cursor.close()

    return prepare


def _begin_explicitly(connection: Connection) -> None:
    connection.exec_driver_sql("BEGIN")


def _decimal_key(stored: str | None) -> str | None:
    """A text whose order equals the numeric order of the exact decimal it spells."""
    if stored is None:
        return None
    try:
        number = Decimal(stored)
    except InvalidOperation:
        return None
    if not number.is_finite():
        return None
    if number == 0:
        return "B"
    sign, digits, exponent = number.normalize().as_tuple()
    assert isinstance(exponent, int)
    magnitude = len(digits) + exponent - 1 + _DECIMAL_OFFSET
    if sign == 0:
        return f"C{magnitude:08d}{''.join(map(str, digits))}"
    return f"A{10**8 - 1 - magnitude:08d}{''.join(str(9 - digit) for digit in digits)}~"


def _failed(error: SQLAlchemyError) -> ExecutionError:
    if isinstance(error, DBAPIError):
        return ExecutionError(f"The operation failed ({type(error.orig).__name__}).")
    return ExecutionError("The operation failed.")


def _declared_type(entity: type[SQLModel], name: str) -> str:
    return declaration_of(entity).field(name).type


def _key(value: object) -> str | None:
    if isinstance(value, Decimal | int):
        return _decimal_key(format(Decimal(value), "f"))
    return None


def _compare(
    entity: type[SQLModel], name: str, operator: FilterOperator, value: object
) -> ColumnElement[bool]:
    """One condition on one Field, with the comparison semantics the Filter vocabulary defines."""
    column = table_of(entity).c[name]
    if operator is FilterOperator.IS_NULL:
        return column.is_(None)
    if operator is FilterOperator.IS_NOT_NULL:
        return column.is_not(None)
    if operator in (
        FilterOperator.CONTAINS,
        FilterOperator.STARTS_WITH,
        FilterOperator.ENDS_WITH,
    ):
        # Text matching is case-sensitive, so it avoids LIKE (which folds ASCII case on this Engine).
        needle = str(value)
        if operator is FilterOperator.CONTAINS:
            return func.instr(column, needle) > 0
        if not needle:
            return column.is_not(None)
        if operator is FilterOperator.STARTS_WITH:
            return func.substr(column, 1, len(needle)) == needle
        return func.substr(column, -len(needle)) == needle
    exact = _declared_type(entity, name) == "decimal"
    left = func.decimal_key(column) if exact else column
    if operator is FilterOperator.IN:
        return left.in_(
            [_key(item) if exact else item for item in cast(Iterable[object], value)]
        )
    bound = _key(value) if exact else value
    match operator:
        case FilterOperator.EQUALS:
            return left == bound
        case FilterOperator.NOT_EQUALS:
            return left != bound
        case FilterOperator.GREATER_THAN:
            return left > bound
        case FilterOperator.GREATER_OR_EQUAL:
            return left >= bound
        case FilterOperator.LESS_THAN:
            return left < bound
        case _:
            return left <= bound


def _where(
    entity: type[SQLModel], filters: Sequence[Filter], combination: FilterCombination
) -> list[ColumnElement[bool]]:
    conditions = [
        _compare(entity, item.field.key, item.operator, item.value) for item in filters
    ]
    if not conditions:
        return []
    return [
        and_(*conditions) if combination is FilterCombination.AND else or_(*conditions)
    ]


def add(
    handle: Engine, entity: type[SQLModel], values: Mapping[str, Any]
) -> dict[str, Any]:
    """Store one new record and return the stored row, including the values storage generated."""
    table = table_of(entity)
    try:
        with handle.begin() as connection:
            return dict(
                connection.execute(insert(table).values(**values).returning(*table.c))
                .mappings()
                .one()
            )
    except SQLAlchemyError as error:
        raise _failed(error) from None


def get(handle: Engine, entity: type[SQLModel], identity: int) -> dict[str, Any] | None:
    """The stored row with the given identity, or null when there is none."""
    table = table_of(entity)
    primary_key = declaration_of(entity).primary_key
    try:
        with handle.connect() as connection:
            row = (
                connection.execute(
                    select(table).where(table.c[primary_key] == identity)
                )
                .mappings()
                .first()
            )
    except SQLAlchemyError as error:
        raise _failed(error) from None
    return dict(row) if row is not None else None


def select_rows(
    handle: Engine,
    entity: type[SQLModel],
    filters: Sequence[Filter],
    combination: FilterCombination,
    orders: Sequence[Order] = (),
    limit: int = -1,
) -> list[dict[str, Any]]:
    """The stored rows that the Filters select under the combination, in the Orders' sequence, at most limit.

    Every row is selected when there are no Filters; a limit of zero or below means no limit.
    """
    table = table_of(entity)
    statement = select(table).where(*_where(entity, filters, combination))
    primary_key = declaration_of(entity).primary_key
    for ordering in orders:
        name = ordering.field.key
        key = (
            func.decimal_key(table.c[name])
            if _declared_type(entity, name) == "decimal"
            else table.c[name]
        )
        statement = statement.order_by(
            key.asc() if ordering.direction is OrderDirection.ASCENDING else key.desc()
        )
    if primary_key not in [ordering.field.key for ordering in orders]:
        statement = statement.order_by(
            table.c[primary_key].asc()
        )  # ties never fall back to storage order
    if limit > 0:
        statement = statement.limit(limit)
    try:
        with handle.connect() as connection:
            return [dict(row) for row in connection.execute(statement).mappings()]
    except SQLAlchemyError as error:
        raise _failed(error) from None


def update(
    handle: Engine, entity: type[SQLModel], identity: int, values: Mapping[str, Any]
) -> dict[str, Any] | None:
    """Replace the given values of the record with the given identity; return the stored row or null."""
    table = table_of(entity)
    primary_key = declaration_of(entity).primary_key
    try:
        with handle.begin() as connection:
            statement = (
                sql_update(table)
                .where(table.c[primary_key] == identity)
                .values(**values)
                .returning(*table.c)
            )
            row = connection.execute(statement).mappings().first()
    except SQLAlchemyError as error:
        raise _failed(error) from None
    return dict(row) if row is not None else None


def delete_by_id(
    handle: Engine, entity: type[SQLModel], identity: int
) -> dict[str, Any] | None:
    """Remove the record with the given identity; return the row as it was just before removal, or null."""
    table = table_of(entity)
    primary_key = declaration_of(entity).primary_key
    try:
        with handle.begin() as connection:
            row = (
                connection.execute(
                    delete(table)
                    .where(table.c[primary_key] == identity)
                    .returning(*table.c)
                )
                .mappings()
                .first()
            )
    except SQLAlchemyError as error:
        raise _failed(error) from None
    return dict(row) if row is not None else None


def count(
    handle: Engine,
    entity: type[SQLModel],
    filters: Sequence[Filter],
    combination: FilterCombination,
) -> int:
    """The number of stored records the Filters select."""
    statement = (
        select(func.count())
        .select_from(table_of(entity))
        .where(*_where(entity, filters, combination))
    )
    try:
        with handle.connect() as connection:
            return int(connection.execute(statement).scalar_one())
    except SQLAlchemyError as error:
        raise _failed(error) from None


def aggregate(
    handle: Engine,
    entity: type[SQLModel],
    function: str,
    name: str,
    filters: Sequence[Filter],
    combination: FilterCombination,
) -> Any:
    """The total, smallest, or largest of one Field over the selected records, ignoring nulls.

    The total is zero (of the Field's own kind) and the others are null when nothing matches.
    """
    table = table_of(entity)
    column = table.c[name]
    declared = _declared_type(entity, name)
    conditions = [*_where(entity, filters, combination), column.is_not(None)]
    try:
        with handle.connect() as connection:
            if function == "sum":
                if (
                    declared == "decimal"
                ):  # exact decimal arithmetic, never floating point
                    values = (
                        connection.execute(select(column).where(*conditions))
                        .scalars()
                        .all()
                    )
                    return sum(values, Decimal(0))
                total = connection.execute(
                    select(func.sum(column)).where(*conditions)
                ).scalar_one()
                return (
                    total if total is not None else (0.0 if declared == "float" else 0)
                )
            if (
                declared == "decimal"
            ):  # compared by exact value through the order-preserving key
                ordering = func.decimal_key(column)
                statement = (
                    select(column)
                    .where(*conditions)
                    .order_by(ordering.asc() if function == "min" else ordering.desc())
                    .limit(1)
                )
                return connection.execute(statement).scalar_one_or_none()
            chosen = func.min(column) if function == "min" else func.max(column)
            return connection.execute(select(chosen).where(*conditions)).scalar_one()
    except SQLAlchemyError as error:
        raise _failed(error) from None


def truncate(handle: Engine, entity: type[SQLModel]) -> int:
    """Remove every record of the Entity, keep its Table, and return the number removed."""
    try:
        with handle.begin() as connection:
            return connection.execute(delete(table_of(entity))).rowcount
    except SQLAlchemyError as error:
        raise _failed(error) from None


def insert_missing(
    handle: Engine,
    records: Sequence[tuple[type[SQLModel], Mapping[str, Any], Mapping[str, Any]]],
) -> int:
    """Insert every record that is not already stored; return how many were inserted.

    Each record is (Entity, the configured values that identify it, every value to store). A record is already
    stored when a row holds the same value for every configured value. A record that is not stored but shares
    a Uniqueness Constraint's values with a stored row conflicts with it: the whole run fails and changes nothing.
    """
    inserted = 0
    try:
        with handle.begin() as connection:
            for entity, configured, values in records:
                table = table_of(entity)
                primary_key = table.c[declaration_of(entity).primary_key]
                identical = [
                    _compare(entity, name, FilterOperator.EQUALS, value)
                    for name, value in configured.items()
                ]
                if connection.execute(select(primary_key).where(*identical)).first():
                    continue
                for group in declaration_of(entity).unique_constraints:
                    if all(name in configured for name in group):
                        keyed = [
                            _compare(
                                entity, name, FilterOperator.EQUALS, configured[name]
                            )
                            for name in group
                        ]
                        if connection.execute(
                            select(primary_key).where(*keyed)
                        ).first():
                            raise ExecutionError(
                                f"A configured {entity.__name__} record conflicts with a stored record."
                            )
                connection.execute(insert(table).values(**values))
                inserted += 1
    except SQLAlchemyError as error:
        raise _failed(error) from None
    return inserted


def _differences(
    inspector: Inspector, entity: type[SQLModel], dialect: Any
) -> list[str]:
    """How an existing Table differs from its Entity's Declaration (categories only, never values)."""
    declaration = declaration_of(entity)
    table = table_of(entity)
    name = table.name
    found: list[str] = []
    columns = inspector.get_columns(name)
    if [column["name"] for column in columns] != [
        declared.name for declared in declaration.fields
    ]:
        return ["fields"]
    for column, declared in zip(columns, declaration.fields, strict=True):
        if (
            str(column["type"]).upper()
            != table.c[declared.name].type.compile(dialect=dialect).upper()
        ):
            found.append("types")
            break
    if any(
        column["nullable"] != declared.nullable
        for column, declared in zip(columns, declaration.fields, strict=True)
        if declared.value_generation is None
    ):
        found.append("nullability")
    if inspector.get_pk_constraint(name)["constrained_columns"] != [
        declaration.primary_key
    ]:
        found.append("primary key")
    relations = {
        (
            key["constrained_columns"][0],
            key["referred_table"],
            key["referred_columns"][0],
        )
        for key in inspector.get_foreign_keys(name)
    }
    if relations != {
        (item.local_field, item.target_entity.replace(" ", ""), item.target_field)
        for item in declaration.relations
    }:
        found.append("relations")
    if {
        tuple(item["column_names"]) for item in inspector.get_unique_constraints(name)
    } != set(declaration.unique_constraints):
        found.append("uniqueness constraints")
    if {
        tuple(item["column_names"])
        for item in inspector.get_indexes(name)
        if not str(item["name"]).startswith("sqlite_autoindex")
    } != set(declaration.indexes):
        found.append("indexes")
    return found


def create_tables(
    handle: Engine, entities: Sequence[type[SQLModel]]
) -> tuple[int, int]:
    """Create the Table of every given Entity that does not exist; return (Tables processed, Tables created).

    An existing Table that differs from its Entity's Declaration stops the command before anything is created.
    """
    tables = [table_of(entity) for entity in entities]
    try:
        with handle.begin() as connection:
            inspector = inspect(connection)
            tables_present = set(inspector.get_table_names())
            for entity in entities:
                name = table_of(entity).name
                if not inspector.has_table(name):
                    continue
                problems = (
                    _differences(inspector, entity, connection.dialect)
                    if name in tables_present
                    else ["kind"]
                )
                if problems:
                    raise DeclarationMismatchError(
                        f"The existing Table for Entity '{entity.__name__}' differs from its Declaration ({', '.join(problems)})."
                    )
            missing = [table for table in tables if not inspector.has_table(table.name)]
            SQLModel.metadata.create_all(connection, tables=missing)
    except SQLAlchemyError:
        raise ExecutionError("Table creation failed.") from None
    return len(tables), len(missing)


def execute(
    handle: Engine, command: str, parameters: Mapping[str, Any] | Sequence[Any] | None
) -> tuple[list[dict[str, Any]] | None, int | None, list[str] | None]:
    """Run one native command; return (rows, affected count, column names), each null when not applicable."""
    try:
        with handle.begin() as connection:
            result = connection.exec_driver_sql(command, parameters or ())
            if result.returns_rows:
                return [dict(row._mapping) for row in result], None, list(result.keys())
            return None, (result.rowcount if result.rowcount >= 0 else None), None
    except DBAPIError as error:
        raise ExecutionError(
            f"The command failed ({type(error.orig).__name__})."
        ) from None
    except SQLAlchemyError:
        raise ExecutionError("The command failed.") from None
