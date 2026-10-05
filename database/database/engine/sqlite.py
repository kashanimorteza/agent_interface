from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import Connection, Engine, and_, create_engine, event, func, insert, inspect, or_
from sqlalchemy import delete as sa_delete
from sqlalchemy import select as sa_select
from sqlalchemy import update as sa_update
from sqlalchemy.exc import SQLAlchemyError

from database.core.data import (
    ConnectionFailureError,
    EngineSettings,
    FilterCombination,
    FilterOperator,
    InstanceSettings,
    OrderDirection,
    Query,
)

ENGINE = "sqlite"


def connect(instance: InstanceSettings, engine: EngineSettings, storage: Path) -> Engine:
    required = engine.parameters.get("required_connection", [])
    absent = [field for field in required if getattr(instance, field) in (None, "")]
    if absent:
        raise ConnectionFailureError(f"The Instance lacks required connection values: {', '.join(absent)}")
    try:
        storage.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        raise ConnectionFailureError("The storage location of the Instance could not be prepared") from None
    handle = create_engine(
        f"{engine.parameters['url_scheme']}:///{storage}",
        connect_args=dict(engine.parameters.get("connect_arguments", {})),
    )
    foreign_keys = bool(engine.parameters.get("foreign_keys", False))

    @event.listens_for(handle, "connect")
    def configure(dbapi_connection: Any, record: Any) -> None:
        dbapi_connection.isolation_level = None
        if foreign_keys:
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    @event.listens_for(handle, "begin")
    def begin(connection: Connection) -> None:
        connection.exec_driver_sql("BEGIN")

    return handle


@contextmanager
def transaction(handle: Engine) -> Iterator[Connection]:
    try:
        connection = handle.connect()
    except SQLAlchemyError:
        raise ConnectionFailureError("The connection to the Instance could not be made") from None
    try:
        with connection.begin():
            yield connection
    finally:
        connection.close()


def _types(entity: Any) -> dict[str, str]:
    return {item.name: item.type for item in entity.declaration.fields}


def _row(cx: Connection, entity: Any, id: int) -> dict[str, Any] | None:
    table = entity.__table__
    found = cx.execute(sa_select(table).where(table.c.id == id)).first()
    return None if found is None else dict(found._mapping)


def add(cx: Connection, entity: Any, values: Mapping[str, Any]) -> dict[str, Any]:
    table = entity.__table__
    stored = cx.execute(insert(table).values({k: v for k, v in values.items() if not (k == "id" and v is None)}))
    key = stored.inserted_primary_key
    row = None if key is None else _row(cx, entity, key[0])
    if row is None:
        raise SQLAlchemyError("The stored record could not be read back")
    return row


def update(cx: Connection, entity: Any, id: int, values: Mapping[str, Any]) -> dict[str, Any] | None:
    table = entity.__table__
    immutable = {item.name for item in entity.declaration.fields if item.immutable}
    changes = {k: v for k, v in values.items() if k not in immutable}
    if cx.execute(sa_update(table).where(table.c.id == id).values(changes)).rowcount == 0:
        return None
    return _row(cx, entity, id)


def get_by_id(cx: Connection, entity: Any, id: int) -> dict[str, Any] | None:
    return _row(cx, entity, id)


def delete(cx: Connection, entity: Any, id: int) -> dict[str, Any] | None:
    row = _row(cx, entity, id)
    if row is not None:
        table = entity.__table__
        cx.execute(sa_delete(table).where(table.c.id == id))
    return row


def _set_active(cx: Connection, entity: Any, id: int, active: bool) -> dict[str, Any] | None:
    table = entity.__table__
    if cx.execute(sa_update(table).where(table.c.id == id).values(is_active=active)).rowcount == 0:
        return None
    return _row(cx, entity, id)


def enable(cx: Connection, entity: Any, id: int) -> dict[str, Any] | None:
    return _set_active(cx, entity, id, True)


def disable(cx: Connection, entity: Any, id: int) -> dict[str, Any] | None:
    return _set_active(cx, entity, id, False)


def truncate(cx: Connection, entity: Any) -> int:
    table = entity.__table__
    removed = cx.execute(sa_select(func.count()).select_from(table)).scalar_one()
    cx.execute(sa_delete(table))
    return removed


def _sql_condition(table: Any, item: Any) -> Any:
    column = table.c[item.field.key]
    operator, value = item.operator, item.value
    if operator is FilterOperator.EQUALS:
        return column == value
    if operator is FilterOperator.NOT_EQUALS:
        return column != value
    if operator is FilterOperator.GREATER_THAN:
        return column > value
    if operator is FilterOperator.GREATER_OR_EQUAL:
        return column >= value
    if operator is FilterOperator.LESS_THAN:
        return column < value
    if operator is FilterOperator.LESS_OR_EQUAL:
        return column <= value
    if operator is FilterOperator.IN:
        return column.in_(value)
    if operator is FilterOperator.IS_NULL:
        return column.is_(None)
    if operator is FilterOperator.IS_NOT_NULL:
        return column.is_not(None)
    if not value:
        return column.is_not(None)
    if operator is FilterOperator.CONTAINS:
        return func.instr(column, value) > 0
    if operator is FilterOperator.STARTS_WITH:
        return func.substr(column, 1, len(value)) == value
    return func.substr(column, -len(value)) == value


def _python_match(row: Mapping[str, Any], item: Any) -> bool:
    value = row[item.field.key]
    operator = item.operator
    if operator is FilterOperator.IS_NULL:
        return value is None
    if operator is FilterOperator.IS_NOT_NULL:
        return value is not None
    if value is None:
        return False
    target = item.value
    if operator is FilterOperator.EQUALS:
        return value == target
    if operator is FilterOperator.NOT_EQUALS:
        return value != target
    if operator is FilterOperator.GREATER_THAN:
        return value > target
    if operator is FilterOperator.GREATER_OR_EQUAL:
        return value >= target
    if operator is FilterOperator.LESS_THAN:
        return value < target
    if operator is FilterOperator.LESS_OR_EQUAL:
        return value <= target
    if operator is FilterOperator.IN:
        return value in target
    if operator is FilterOperator.CONTAINS:
        return target in value
    if operator is FilterOperator.STARTS_WITH:
        return value.startswith(target)
    return value.endswith(target)


def _exact_filters(entity: Any, query: Query) -> bool:
    types = _types(entity)
    return any(types[item.field.key] == "decimal" for item in query.filters)


def _filtered_rows(cx: Connection, entity: Any, query: Query) -> list[dict[str, Any]]:
    table = entity.__table__
    statement = sa_select(table)
    exact = _exact_filters(entity, query)
    if query.filters and not exact:
        combine = and_ if query.combination is FilterCombination.AND else or_
        statement = statement.where(combine(*[_sql_condition(table, item) for item in query.filters]))
    rows = [dict(row._mapping) for row in cx.execute(statement)]
    if query.filters and exact:
        test = all if query.combination is FilterCombination.AND else any
        rows = [row for row in rows if test(_python_match(row, item) for item in query.filters)]
    return rows


def select(cx: Connection, entity: Any, query: Query) -> list[dict[str, Any]]:
    table = entity.__table__
    types = _types(entity)
    exact_filters = _exact_filters(entity, query)
    exact_orders = any(types[order.field.key] == "decimal" for order in query.orders)
    if not exact_filters and not exact_orders:
        statement = sa_select(table)
        if query.filters:
            combine = and_ if query.combination is FilterCombination.AND else or_
            statement = statement.where(combine(*[_sql_condition(table, item) for item in query.filters]))
        keys = [
            table.c[order.field.key].desc()
            if order.direction is OrderDirection.DESCENDING
            else table.c[order.field.key].asc()
            for order in query.orders
        ]
        if all(order.field.key != "id" for order in query.orders):
            keys.append(table.c.id.asc())
        statement = statement.order_by(*keys)
        if query.limit > 0:
            statement = statement.limit(query.limit)
        return [dict(row._mapping) for row in cx.execute(statement)]
    rows = _filtered_rows(cx, entity, query)
    rows.sort(key=lambda row: row["id"])
    for order in reversed(query.orders):
        name = order.field.key
        rows.sort(
            key=lambda row, name=name: (row[name] is not None, row[name]),
            reverse=order.direction is OrderDirection.DESCENDING,
        )
    return rows[: query.limit] if query.limit > 0 else rows


def count(cx: Connection, entity: Any, query: Query) -> int:
    if _exact_filters(entity, query):
        return len(_filtered_rows(cx, entity, query))
    table = entity.__table__
    statement = sa_select(func.count()).select_from(table)
    if query.filters:
        combine = and_ if query.combination is FilterCombination.AND else or_
        statement = statement.where(combine(*[_sql_condition(table, item) for item in query.filters]))
    return cx.execute(statement).scalar_one()


def _aggregate(cx: Connection, entity: Any, name: str, query: Query, kind: str) -> Any:
    field_type = _types(entity)[name]
    if field_type == "decimal" or _exact_filters(entity, query):
        values = [row[name] for row in _filtered_rows(cx, entity, query) if row[name] is not None]
        if kind == "sum":
            return sum(values, {"integer": 0, "float": 0.0, "decimal": Decimal(0)}[field_type])
        if not values:
            return None
        return min(values) if kind == "min" else max(values)
    table = entity.__table__
    function = {"sum": func.sum, "min": func.min, "max": func.max}[kind]
    statement = sa_select(function(table.c[name])).select_from(table)
    if query.filters:
        combine = and_ if query.combination is FilterCombination.AND else or_
        statement = statement.where(combine(*[_sql_condition(table, item) for item in query.filters]))
    value = cx.execute(statement).scalar()
    if kind == "sum" and value is None:
        return 0.0 if field_type == "float" else 0
    return value


def total(cx: Connection, entity: Any, name: str, query: Query) -> Any:
    return _aggregate(cx, entity, name, query, "sum")


def smallest(cx: Connection, entity: Any, name: str, query: Query) -> Any:
    return _aggregate(cx, entity, name, query, "min")


def largest(cx: Connection, entity: Any, name: str, query: Query) -> Any:
    return _aggregate(cx, entity, name, query, "max")


def execute_command(
    cx: Connection, command: str, parameters: Mapping[str, Any] | Sequence[Any] | None
) -> tuple[list[dict[str, Any]] | None, int | None, list[str] | None]:
    bound = () if parameters is None else dict(parameters) if isinstance(parameters, Mapping) else tuple(parameters)
    result = cx.exec_driver_sql(command, bound)
    if result.returns_rows:
        return [dict(row._mapping) for row in result], None, list(result.keys())
    return None, max(result.rowcount, 0), None


def create_tables(cx: Connection, tables: Sequence[Any]) -> list[str]:
    existing = set(inspect(cx).get_table_names())
    missing = [table for table in tables if table.name not in existing]
    if missing:
        missing[0].metadata.create_all(cx, tables=missing, checkfirst=False)
    return [table.name for table in missing]


_DECLARED_FAMILIES = {
    "integer": "integer",
    "string": "text",
    "decimal": "text",
    "uuid": "text",
    "boolean": "boolean",
    "float": "float",
    "datetime": "datetime",
    "date": "date",
    "time": "time",
}
_STORED_FAMILIES = (
    ("DATETIME", "datetime"),
    ("BOOL", "boolean"),
    ("INT", "integer"),
    ("FLOAT", "float"),
    ("REAL", "float"),
    ("DATE", "date"),
    ("TIME", "time"),
    ("CHAR", "text"),
    ("TEXT", "text"),
)


def declared_family(type_name: str) -> str:
    return _DECLARED_FAMILIES[type_name]


def _stored_family(column_type: Any) -> str:
    text = str(column_type).upper()
    return next((family for key, family in _STORED_FAMILIES if key in text), text.lower())


def describe_tables(cx: Connection, names: Sequence[str]) -> dict[str, dict[str, Any]]:
    inspector = inspect(cx)
    existing = set(inspector.get_table_names())
    described: dict[str, dict[str, Any]] = {}
    for name in names:
        if name not in existing:
            continue
        indexes = inspector.get_indexes(name)
        described[name] = {
            "columns": [
                (column["name"], _stored_family(column["type"]), bool(column["nullable"]))
                for column in inspector.get_columns(name)
            ],
            "primary_key": list(inspector.get_pk_constraint(name)["constrained_columns"]),
            "unique": {tuple(item["column_names"]) for item in inspector.get_unique_constraints(name)}
            | {tuple(item["column_names"]) for item in indexes if item["unique"]},
            "foreign_keys": {
                (item["constrained_columns"][0], item["referred_table"], item["referred_columns"][0])
                for item in inspector.get_foreign_keys(name)
            },
            "indexes": {tuple(item["column_names"]) for item in indexes if not item["unique"]},
        }
    return described


def find(cx: Connection, entity: Any, criteria: Mapping[str, Any]) -> dict[str, Any] | None:
    table = entity.__table__
    types = _types(entity)
    exact = {name: value for name, value in criteria.items() if types[name] == "decimal"}
    statement = sa_select(table).where(
        *[table.c[name] == value for name, value in criteria.items() if name not in exact]
    )
    for row in cx.execute(statement):
        values = dict(row._mapping)
        if all(values[name] is not None and values[name] == value for name, value in exact.items()):
            return values
    return None
