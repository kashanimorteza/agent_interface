"""Engine implementation for SQLite (internal layer, not a consumer surface)."""

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import model.interface  # noqa: F401  (registers every Entity's storage structure)
from model.declaration import Declaration
from sqlalchemy import Engine as SqlEngine
from sqlalchemy import and_, delete, event, func, or_, text
from sqlmodel import Session, SQLModel, create_engine, select

from database.interface import (
    CommandResult,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)


class Engine:
    """Carries out Database Operations against one SQLite Instance."""

    def __init__(
        self,
        instance: Mapping[str, Any],
        parameters: Mapping[str, Any],
        directory: Path,
    ) -> None:
        self.location = directory / instance["database"]
        self.location.parent.mkdir(parents=True, exist_ok=True)
        connect_args = {"check_same_thread": parameters["check_same_thread"]}
        self.sql: SqlEngine = create_engine(
            f"{parameters['url_scheme']}:///{self.location}", connect_args=connect_args
        )
        if parameters["foreign_keys"]:

            @event.listens_for(self.sql, "connect")
            def _enable_foreign_keys(connection: Any, _record: Any) -> None:
                connection.execute("PRAGMA foreign_keys=ON")

    def create_structure(self) -> None:
        """Create the storage structure of every Entity that does not yet exist."""
        SQLModel.metadata.create_all(self.sql)

    @contextmanager
    def transaction(self) -> Iterator[Session]:
        """Run work atomically: everything is committed on success, nothing on failure."""
        with Session(self.sql, expire_on_commit=False) as session:
            try:
                yield session
                session.commit()
            except BaseException:
                session.rollback()
                raise

    def add(self, entity: SQLModel) -> SQLModel:
        """Store a new record and return the created Entity."""
        created = type(entity).model_validate(_values_for_add(entity))
        with self.transaction() as session:
            session.add(created)
            session.flush()
            session.refresh(created)
        return created

    def get_by_id(self, entity: type[SQLModel], id: int) -> SQLModel | None:
        """Return the record with this id, or None."""
        with self.transaction() as session:
            return session.get(entity, id)

    def list_(
        self,
        entity: type[SQLModel],
        *,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | str,
        orders: Sequence[Order],
        limit: int | None = None,
    ) -> list[SQLModel]:
        """Return the matching records, ordered, and capped by the limit when given."""
        statement = select(entity)
        conditions = [_condition(entity, f) for f in filters or ()]
        if conditions:
            joiner = (
                and_ if FilterCombination(combination) is FilterCombination.AND else or_
            )
            statement = statement.where(joiner(*conditions))
        for order in orders:
            column = _column(entity, order.field)
            descending = OrderDirection(order.direction) is OrderDirection.DESCENDING
            statement = statement.order_by(
                column.desc() if descending else column.asc()
            )
        if limit is not None:
            statement = statement.limit(limit)
        with self.transaction() as session:
            return list(session.exec(statement).all())

    def update(self, entity: SQLModel) -> SQLModel | None:
        """Change only the supplied mutable Fields of the record with this id."""
        entity_type = type(entity)
        declaration: Declaration = entity_type.declaration  # type: ignore[attr-defined]
        record_id = getattr(entity, "id", None)
        if record_id is None:
            raise ValueError("Update requires the id of the record to change")
        mutable = {
            f.name for f in declaration.fields if f.name != "id" and not f.immutable
        }
        changes = {
            n: getattr(entity, n) for n in entity.model_fields_set if n in mutable
        }
        with self.transaction() as session:
            record = session.get(entity_type, record_id)
            if record is None:
                return None
            entity_type.model_validate({**record.model_dump(), **changes})
            for name, value in changes.items():
                setattr(record, name, value)
            session.add(record)
            session.flush()
            session.refresh(record)
            return record

    def delete(self, entity: type[SQLModel], id: int) -> bool:
        """Remove the record with this id; report whether one was removed."""
        with self.transaction() as session:
            record = session.get(entity, id)
            if record is None:
                return False
            session.delete(record)
            return True

    def enable(self, entity: type[SQLModel], id: int) -> SQLModel | None:
        """Mark the record active."""
        return self._set_active(entity, id, True)

    def disable(self, entity: type[SQLModel], id: int) -> SQLModel | None:
        """Mark the record inactive."""
        return self._set_active(entity, id, False)

    def _set_active(
        self, entity: type[SQLModel], id: int, active: bool
    ) -> SQLModel | None:
        with self.transaction() as session:
            record = session.get(entity, id)
            if record is None:
                return None
            record.is_active = active
            session.add(record)
            session.flush()
            session.refresh(record)
            return record

    def count(self, entity: type[SQLModel]) -> int:
        """Return the number of records."""
        with self.transaction() as session:
            return session.exec(select(func.count()).select_from(entity)).one()

    def sum_(self, entity: type[SQLModel], field: str) -> Any:
        """Return the total of a numeric Field, ignoring nulls; 0 when nothing is usable."""
        with self.transaction() as session:
            total = session.exec(select(func.sum(_column(entity, field)))).one()
        return 0 if total is None else total

    def min_(self, entity: type[SQLModel], field: str) -> Any:
        """Return the smallest value of a Field, ignoring nulls; None when nothing is usable."""
        with self.transaction() as session:
            return session.exec(select(func.min(_column(entity, field)))).one()

    def max_(self, entity: type[SQLModel], field: str) -> Any:
        """Return the largest value of a Field, ignoring nulls; None when nothing is usable."""
        with self.transaction() as session:
            return session.exec(select(func.max(_column(entity, field)))).one()

    def truncate(self, entity: type[SQLModel]) -> int:
        """Remove every record, keep the structure, and return how many were removed."""
        with self.transaction() as session:
            return session.exec(delete(entity)).rowcount  # type: ignore[attr-defined]

    def execute_command(
        self, command: str, parameters: Mapping[str, Any] | None = None
    ) -> CommandResult:
        """Run one SQL command and report its rows or affected count."""
        with self.transaction() as session:
            result = session.connection().execute(text(command), dict(parameters or {}))
            if result.returns_rows:
                return CommandResult(rows=[dict(row._mapping) for row in result])
            return CommandResult(affected_count=result.rowcount)


def _column(entity: type[SQLModel], name: str) -> Any:
    table: Any = entity.__table__  # type: ignore[attr-defined]
    if name not in table.c:
        raise ValueError(f"'{entity.__name__}' has no Field '{name}'")
    return table.c[name]


def _condition(entity: type[SQLModel], filter_: Filter) -> Any:
    column = _column(entity, filter_.field)
    value = filter_.value
    match FilterOperator(filter_.operator):
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
            return column.in_(list(value))
        case FilterOperator.CONTAINS:
            return column.contains(value, autoescape=True)
        case FilterOperator.STARTS_WITH:
            return column.startswith(value, autoescape=True)
        case FilterOperator.ENDS_WITH:
            return column.endswith(value, autoescape=True)
        case FilterOperator.IS_NULL:
            return column.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return column.is_not(None)


def _values_for_add(entity: SQLModel) -> dict[str, Any]:
    """Apply Value Generation, then Default Values, then the required and nullability rules."""
    declaration: Declaration = type(entity).declaration  # type: ignore[attr-defined]
    supplied = entity.model_fields_set
    values: dict[str, Any] = {}
    for field in declaration.fields:
        name = field.name
        if field.value_generation is not None:
            if getattr(entity, name, None) is not None:
                raise ValueError(f"'{name}' is generated and cannot be supplied")
            continue
        if name in supplied:
            value = getattr(entity, name)
            if value is None and not field.nullable:
                raise ValueError(f"'{name}' is required and cannot be null")
            values[name] = value
        elif field.has_default:
            values[name] = field.default
        elif field.nullable:
            values[name] = None
        else:
            raise ValueError(f"'{name}' is required")
    return values
