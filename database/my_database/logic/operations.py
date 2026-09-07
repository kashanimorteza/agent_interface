"""The generic, Model-driven operation pipeline.

One pipeline serves every Model: the caller supplies a Model type or Model
instance from the public Model package, the operation, and its criteria.
What a Model's own data determines is checked by the validation the Model
package publishes, never by a second copy of those rules kept here. Rows are
converted back into Model instances, and the stored representation of a
credential never reaches a consumer.
"""

from __future__ import annotations

import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

from my_model import InvalidValue, Model, validate_change, validate_state
from sqlalchemy import Connection, Row, delete, insert, select, text, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..adapter.connection import StorageAdapter
from ..errors import (
    ConstraintViolation,
    DatabaseError,
    InvalidData,
    InvalidOperation,
    NotFound,
)
from .credentials import CredentialTransformer
from .mapping import StorageMapping, TableMapping

#: What a consumer receives in place of a stored credential.
CREDENTIAL_MASK = "********"

STATUS_ACTIONS = {"enable": True, "disable": False}

#: Only data statements may be executed. Everything else, structural changes
#: and transaction control included, belongs elsewhere.
DATA_STATEMENTS = frozenset({"select", "insert", "update", "delete", "with", "values", "explain"})

_COMMENTS = re.compile(r"--[^\n]*|/\*.*?\*/", re.S)


class Pipeline:
    def __init__(self, mapping: StorageMapping, adapter: StorageAdapter,
                 credentials: CredentialTransformer) -> None:
        self.mapping = mapping
        self.adapter = adapter
        self.credentials = credentials

    # -- Model identity ------------------------------------------------------

    def resolve_model(self, model: type[Model] | Model) -> type[Model]:
        """A Model type from a Model type or instance; anything else is rejected."""
        if isinstance(model, Model):
            model = type(model)
        if not (isinstance(model, type) and issubclass(model, Model) and model is not Model):
            raise InvalidOperation(
                f"expected a Model type or instance from the Model package, got {model!r}"
            )
        if model not in self.mapping.tables:
            raise InvalidOperation(f"{model.__name__} is not a persistent Model")
        return model

    def _table(self, model: type[Model] | Model) -> TableMapping:
        return self.mapping.for_model(self.resolve_model(model))

    # -- connections ---------------------------------------------------------

    @contextmanager
    def _connection(self, instance: Any, given: Connection | None) -> Iterator[Connection]:
        """The caller's connection when one is supplied, otherwise an atomic one."""
        if given is not None:
            yield given
        else:
            with self.adapter.connect(instance) as connection:
                yield connection

    @staticmethod
    def _guarded(fn):
        try:
            return fn()
        except IntegrityError as exc:
            raise ConstraintViolation(str(exc.orig)) from exc
        except SQLAlchemyError as exc:
            raise DatabaseError(str(exc)) from exc

    # -- operations ----------------------------------------------------------

    def create(self, model: type[Model] | Model, data: Mapping[str, Any] | None = None,
               instance: Any = None, conn: Connection | None = None) -> Model:
        """Store a new record from a Model instance, or from a Model and its data."""
        if isinstance(model, Model):
            if data is not None:
                raise InvalidOperation("supply either a Model instance or a Model type and its data")
            value = model
            tm = self._table(value)
        else:
            tm = self._table(model)
            if data is None:
                raise InvalidOperation("creating from a Model type needs its data")
            state = self._validated_state(tm.model, data)
            if state.pending:
                raise InvalidData(
                    f"{tm.model.__name__}: {', '.join(sorted(state.pending))} still awaits "
                    f"declared generation and cannot be stored",
                    tuple(sorted(state.pending)),
                )
            value = state.resolved()
        stored = self._to_storage(tm, value.model_dump())
        if stored.get(tm.identifier) is None:
            stored.pop(tm.identifier, None)

        def run():
            with self._connection(instance, conn) as connection:
                result = connection.execute(insert(tm.table).values(**stored))
                key = result.inserted_primary_key[0] if result.inserted_primary_key else stored[tm.identifier]
                return self._fetch(connection, tm, key)

        return self._guarded(run)

    def read(self, model: type[Model] | Model, key: Any, instance: Any = None,
             conn: Connection | None = None) -> Model:
        tm = self._table(model)

        def run():
            with self._connection(instance, conn) as connection:
                return self._fetch(connection, tm, key)

        return self._guarded(run)

    def list(self, model: type[Model] | Model, criteria: Mapping[str, Any] | None = None,
             instance: Any = None, conn: Connection | None = None) -> list[Model]:
        tm = self._table(model)
        criteria = dict(criteria or {})
        unknown = set(criteria) - set(tm.columns)
        if unknown:
            raise InvalidOperation(f"{tm.model.__name__} declares no field {sorted(unknown)}")
        for name in criteria:
            if name in tm.at_rest:
                raise InvalidOperation(
                    f"{tm.model.__name__}.{name} is a credential and cannot be a criterion"
                )
        statement = select(tm.table).order_by(tm.table.c[tm.identifier])
        for name, value in criteria.items():
            statement = statement.where(tm.table.c[name] == value)

        def run():
            with self._connection(instance, conn) as connection:
                return [self._to_model(tm, row) for row in connection.execute(statement)]

        return self._guarded(run)

    def update(self, model: type[Model] | Model, key: Any, changes: Mapping[str, Any],
               instance: Any = None, conn: Connection | None = None) -> Model:
        tm = self._table(model)
        change = self._validated_change(tm.model, changes)
        if change.pending:
            raise InvalidData(
                f"{tm.model.__name__}: {', '.join(sorted(change.pending))} still awaits "
                f"declared generation and cannot be stored",
                tuple(sorted(change.pending)),
            )
        stored = self._to_storage(tm, change.changes)

        def run():
            with self._connection(instance, conn) as connection:
                self._fetch(connection, tm, key)  # the record must exist
                if stored:
                    connection.execute(
                        update(tm.table).where(tm.table.c[tm.identifier] == key).values(**stored)
                    )
                return self._fetch(connection, tm, key)

        return self._guarded(run)

    def delete(self, model: type[Model] | Model, key: Any, instance: Any = None,
               conn: Connection | None = None) -> None:
        tm = self._table(model)

        def run():
            with self._connection(instance, conn) as connection:
                result = connection.execute(delete(tm.table).where(tm.table.c[tm.identifier] == key))
                if result.rowcount == 0:
                    raise NotFound(f"{tm.model.__name__} {key!r} does not exist")

        self._guarded(run)

    def status(self, model: type[Model] | Model, key: Any, action: str, instance: Any = None,
               conn: Connection | None = None) -> Model:
        tm = self._table(model)
        if "status" not in tm.columns:
            raise InvalidOperation(f"{tm.model.__name__} declares no status field")
        if action not in STATUS_ACTIONS:
            raise InvalidOperation(f"status accepts 'enable' or 'disable', not {action!r}")
        return self.update(model, key, {"status": STATUS_ACTIONS[action]}, instance, conn)

    def execute(self, statement: str, parameters: Mapping[str, Any] | None = None,
                engine: str | None = None, instance: Any = None,
                conn: Connection | None = None) -> list[dict[str, Any]]:
        """Run one parameterized data command; values are bound, never interpolated."""
        if not isinstance(statement, str):
            raise InvalidOperation("the statement must be text")
        self._require_data_statement(statement)
        if engine is not None:
            actual = self.adapter.instances.profile(instance).engine
            if engine != actual:
                raise InvalidOperation(
                    f"this command is written for the {engine} Engine; the selected Instance "
                    f"uses {actual}"
                )

        def run():
            with self._connection(instance, conn) as connection:
                result = connection.execute(text(statement), dict(parameters or {}))
                if not result.returns_rows:
                    return []
                return [dict(row._mapping) for row in result]

        return self._guarded(run)

    @staticmethod
    def _require_data_statement(statement: str) -> None:
        stripped = _COMMENTS.sub(" ", statement).strip().rstrip(";").strip()
        if ";" in stripped:
            raise InvalidOperation("only one command may be executed at a time")
        leading = stripped.split(None, 1)[0].lower() if stripped else ""
        if leading not in DATA_STATEMENTS:
            raise InvalidOperation(
                f"{leading or 'an empty command'!r} is not a data command; a change to the "
                f"storage structure belongs to the migration history"
            )

    # -- credentials ---------------------------------------------------------

    def verify_credential(self, model: type[Model] | Model, key: Any, field: str, given: str,
                          instance: Any = None, conn: Connection | None = None) -> bool:
        tm, mode = self._credential(model, field)

        def run():
            with self._connection(instance, conn) as connection:
                stored = self._stored_value(connection, tm, key, field)
            return stored is not None and self.credentials.verify(mode, stored, given)

        return self._guarded(run)

    def recover_credential(self, model: type[Model] | Model, key: Any, field: str,
                           instance: Any = None, conn: Connection | None = None) -> str:
        tm, mode = self._credential(model, field)

        def run():
            with self._connection(instance, conn) as connection:
                stored = self._stored_value(connection, tm, key, field)
            if stored is None:
                raise NotFound(f"{tm.model.__name__} {key!r} has no {field}")
            return self.credentials.recover(mode, stored)

        return self._guarded(run)

    def _credential(self, model: type[Model] | Model, field: str) -> tuple[TableMapping, str]:
        tm = self._table(model)
        if field not in tm.at_rest:
            raise InvalidOperation(f"{tm.model.__name__}.{field} is not a credential field")
        return tm, tm.at_rest[field]

    # -- shared Model validation --------------------------------------------

    @staticmethod
    def _validated_state(model: type[Model], data: Mapping[str, Any]):
        try:
            return validate_state(model, data)
        except InvalidValue as invalid:
            raise InvalidData(str(invalid), invalid.fields) from None

    @staticmethod
    def _validated_change(model: type[Model], data: Mapping[str, Any]):
        try:
            return validate_change(model, data)
        except InvalidValue as invalid:
            raise InvalidData(str(invalid), invalid.fields) from None

    # -- conversions ---------------------------------------------------------

    def _to_storage(self, tm: TableMapping, data: Mapping[str, Any]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for name, value in data.items():
            mode = tm.at_rest.get(name)
            if mode is not None:
                if value == CREDENTIAL_MASK:
                    continue  # the mask is never stored
                if not isinstance(value, str):
                    raise InvalidData(f"{tm.model.__name__}.{name} must be given as text", (name,))
                value = self.credentials.transform(mode, value)
            out[name] = value
        return out

    def _to_model(self, tm: TableMapping, row: Row) -> Model:
        data = dict(row._mapping)
        for name in tm.at_rest:
            if data.get(name) is not None:
                data[name] = CREDENTIAL_MASK
        return tm.model.model_validate(data)

    # -- helpers -------------------------------------------------------------

    def _fetch(self, connection: Connection, tm: TableMapping, key: Any) -> Model:
        row = connection.execute(select(tm.table).where(tm.table.c[tm.identifier] == key)).first()
        if row is None:
            raise NotFound(f"{tm.model.__name__} {key!r} does not exist")
        return self._to_model(tm, row)

    @staticmethod
    def _stored_value(connection: Connection, tm: TableMapping, key: Any, field: str) -> str | None:
        row = connection.execute(
            select(tm.table.c[field]).where(tm.table.c[tm.identifier] == key)
        ).first()
        if row is None:
            raise NotFound(f"{tm.model.__name__} {key!r} does not exist")
        return row[0]
