"""The generic, Model-driven operation pipeline.

One pipeline serves every Model: the caller supplies a Model type or instance
from the public Model package, the operation, and its criteria. Rows are
converted back into Model instances; the stored representation of a
credential is never returned.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from my_model import Model
from sqlalchemy import Row, delete, insert, select, text, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..adapter.connection import StorageAdapter
from ..errors import ConstraintViolation, DatabaseError, InvalidOperation, NotFound
from .credentials import CredentialTransformer
from .mapping import StorageMapping, TableMapping

M = TypeVar("M", bound=Model)

#: The value returned in place of a stored credential.
CREDENTIAL_MASK = "********"
STATUS_ACTIONS = {"enable": True, "disable": False}


class Pipeline:
    def __init__(self, mapping: StorageMapping, adapter: StorageAdapter, credentials: CredentialTransformer) -> None:
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

    # -- conversions ---------------------------------------------------------

    def _to_storage(self, tm: TableMapping, data: Mapping[str, Any], *, partial: bool) -> dict[str, Any]:
        unknown = set(data) - set(tm.columns)
        if unknown:
            raise InvalidOperation(f"{tm.model.__name__} has no field {sorted(unknown)}")
        out: dict[str, Any] = {}
        for name, value in data.items():
            mode = tm.at_rest.get(name)
            if mode is not None:
                if partial and value == CREDENTIAL_MASK:
                    continue  # the mask is never stored
                if not isinstance(value, str):
                    raise InvalidOperation(f"{tm.model.__name__}.{name} must be given as text")
                value = self.credentials.transform(mode, value)
            out[name] = value
        return out

    def _to_model(self, tm: TableMapping, row: Row) -> Model:
        data = dict(row._mapping)
        for name in tm.at_rest:
            if data.get(name) is not None:
                data[name] = CREDENTIAL_MASK
        return tm.model.model_validate(data)

    @staticmethod
    def _run(fn):
        try:
            return fn()
        except IntegrityError as exc:
            raise ConstraintViolation(str(exc.orig)) from exc
        except SQLAlchemyError as exc:
            raise DatabaseError(str(exc)) from exc

    # -- operations ----------------------------------------------------------

    def create(self, value: Model, instance: str | None = None) -> Model:
        if not isinstance(value, Model):
            raise InvalidOperation("create takes a Model instance")
        tm = self._table(value)
        data = value.model_dump()
        if data.get(tm.primary_key) is None:
            data.pop(tm.primary_key, None)
        stored = self._to_storage(tm, data, partial=False)

        def run():
            with self.adapter.connect(instance) as conn:
                result = conn.execute(insert(tm.table).values(**stored))
                key = result.inserted_primary_key[0] if result.inserted_primary_key else stored[tm.primary_key]
                return self._fetch(conn, tm, key)

        return self._run(run)

    def read(self, model: type[Model] | Model, key: Any, instance: str | None = None) -> Model:
        tm = self._table(model)

        def run():
            with self.adapter.connect(instance) as conn:
                return self._fetch(conn, tm, key)

        return self._run(run)

    def list(self, model: type[Model] | Model, criteria: Mapping[str, Any] | None = None,
             instance: str | None = None) -> list[Model]:
        tm = self._table(model)
        criteria = dict(criteria or {})
        unknown = set(criteria) - set(tm.columns)
        if unknown:
            raise InvalidOperation(f"{tm.model.__name__} has no field {sorted(unknown)}")
        for name in criteria:
            if name in tm.at_rest:
                raise InvalidOperation(f"{tm.model.__name__}.{name} is a credential and cannot be a criterion")
        stmt = select(tm.table).order_by(tm.table.c[tm.primary_key])
        for name, value in criteria.items():
            stmt = stmt.where(tm.table.c[name] == value)

        def run():
            with self.adapter.connect(instance) as conn:
                return [self._to_model(tm, row) for row in conn.execute(stmt)]

        return self._run(run)

    def update(self, model: type[Model] | Model, key: Any, changes: Mapping[str, Any],
               instance: str | None = None) -> Model:
        tm = self._table(model)
        if tm.primary_key in changes:
            raise InvalidOperation("the identifier cannot be changed")
        stored = self._to_storage(tm, changes, partial=True)
        # validate the resulting value against the Model before storing it
        current = self.read(model, key, instance).model_dump()
        merged = {**current, **{k: v for k, v in changes.items() if k not in tm.at_rest}}
        for name in tm.at_rest:
            merged[name] = "" if merged.get(name) is None else str(merged[name])
        tm.model.model_validate(merged)

        def run():
            with self.adapter.connect(instance) as conn:
                if stored:
                    conn.execute(update(tm.table).where(tm.table.c[tm.primary_key] == key).values(**stored))
                return self._fetch(conn, tm, key)

        return self._run(run)

    def delete(self, model: type[Model] | Model, key: Any, instance: str | None = None) -> None:
        tm = self._table(model)

        def run():
            with self.adapter.connect(instance) as conn:
                result = conn.execute(delete(tm.table).where(tm.table.c[tm.primary_key] == key))
                if result.rowcount == 0:
                    raise NotFound(f"{tm.model.__name__} {key!r} does not exist")

        self._run(run)

    def status(self, model: type[Model] | Model, key: Any, action: str, instance: str | None = None) -> Model:
        tm = self._table(model)
        if "status" not in tm.columns:
            raise InvalidOperation(f"{tm.model.__name__} declares no status field")
        if action not in STATUS_ACTIONS:
            raise InvalidOperation(f"status accepts 'enable' or 'disable', not {action!r}")
        return self.update(model, key, {"status": STATUS_ACTIONS[action]}, instance)

    def execute(self, statement: str, parameters: Mapping[str, Any] | None = None,
                instance: str | None = None) -> list[dict[str, Any]]:
        """Run one parameterized command; values are bound, never interpolated."""
        if not isinstance(statement, str):
            raise InvalidOperation("the statement must be text")

        def run():
            with self.adapter.connect(instance) as conn:
                result = conn.execute(text(statement), dict(parameters or {}))
                if not result.returns_rows:
                    return []
                return [dict(row._mapping) for row in result]

        return self._run(run)

    # -- credentials ---------------------------------------------------------

    def verify_credential(self, model: type[Model] | Model, key: Any, field: str, given: str,
                          instance: str | None = None) -> bool:
        tm, mode = self._credential(model, field)

        def run():
            with self.adapter.connect(instance) as conn:
                stored = self._stored_value(conn, tm, key, field)
            return stored is not None and self.credentials.verify(mode, stored, given)

        return self._run(run)

    def recover_credential(self, model: type[Model] | Model, key: Any, field: str,
                           instance: str | None = None) -> str:
        tm, mode = self._credential(model, field)

        def run():
            with self.adapter.connect(instance) as conn:
                stored = self._stored_value(conn, tm, key, field)
            if stored is None:
                raise NotFound(f"{tm.model.__name__} {key!r} has no {field}")
            return self.credentials.recover(mode, stored)

        return self._run(run)

    def _credential(self, model: type[Model] | Model, field: str) -> tuple[TableMapping, str]:
        tm = self._table(model)
        if field not in tm.at_rest:
            raise InvalidOperation(f"{tm.model.__name__}.{field} is not a credential field")
        return tm, tm.at_rest[field]

    # -- helpers -------------------------------------------------------------

    def _fetch(self, conn, tm: TableMapping, key: Any) -> Model:
        row = conn.execute(select(tm.table).where(tm.table.c[tm.primary_key] == key)).first()
        if row is None:
            raise NotFound(f"{tm.model.__name__} {key!r} does not exist")
        return self._to_model(tm, row)

    @staticmethod
    def _stored_value(conn, tm: TableMapping, key: Any, field: str) -> str | None:
        row = conn.execute(
            select(tm.table.c[field]).where(tm.table.c[tm.primary_key] == key)
        ).first()
        if row is None:
            raise NotFound(f"{tm.model.__name__} {key!r} does not exist")
        return row[0]
