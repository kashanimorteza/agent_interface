"""The one generic public Database Interface (Database Principle 1 & 8): every mapped Domain
Definition is reached through this same Model-driven pipeline, never a per-Domain-Definition
entry point."""

from __future__ import annotations

import typing

import pydantic
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from database import observability
from database.adapter import StorageAdapter
from database.credentials import TRANSFORM_ON_WRITE, decrypt_value
from database.errors import (
    DuplicateRecordError,
    NotFoundError,
    ReferencedRecordMissingError,
    UnsupportedOperationError,
)
from database.mapping import MAPPINGS, TABLES, ModelMapping
from database.registry import InstanceRegistry
from database.transaction import Transaction

ModelType = type[pydantic.BaseModel]

PROTECTED_VALUE_PLACEHOLDER = "***protected***"
"""What a credential Field reads back as through the standard generic Interface (Database
Principle 12 — Database never exposes a credential representation through its public interface).
The caller's own `create`/`update` call still receives back the value it supplied itself, since
echoing a caller's own input exposes nothing they did not already have."""


def _to_storage_values(record: pydantic.BaseModel, *, include_id: bool) -> dict[str, object]:
    data = record.model_dump(mode="python")
    credential_storage = type(record).credential_storage()
    for field, mode in credential_storage.items():
        value = data.get(field)
        if value is not None:
            data[field] = TRANSFORM_ON_WRITE[mode](value)
    if not include_id:
        data.pop("id", None)
    return data


def _from_storage_row(row: typing.Mapping[str, object], model_cls: ModelType) -> pydantic.BaseModel:
    data = dict(row)
    for field in model_cls.credential_storage():
        if data.get(field) is not None:
            data[field] = PROTECTED_VALUE_PLACEHOLDER
    return model_cls.model_validate(data)


class DatabaseInterface:
    """The public Database boundary (Database Principle 1). Consumers import a Model type or
    instance and never see a table, column, connection, or private mapping detail."""

    def __init__(self, adapter: StorageAdapter | None = None) -> None:
        self._adapter = adapter or StorageAdapter()
        self.registry = InstanceRegistry(self._adapter)

    def transaction(self, instance_key: str | None = None) -> Transaction:
        return Transaction(self._adapter, instance_key)

    def _mapping_for(self, model_cls: ModelType) -> tuple[sa.Table, ModelMapping]:
        if model_cls not in MAPPINGS:
            raise UnsupportedOperationError(
                f"{model_cls.__name__} has no Database storage mapping."
            )
        return TABLES[model_cls], MAPPINGS[model_cls]

    def _require_operation(self, model_cls: ModelType, operation: str) -> None:
        if operation not in model_cls.model_operations():
            raise UnsupportedOperationError(
                f"{model_cls.__name__} does not declare the '{operation}' Model Operation."
            )

    def _run(
        self,
        instance_key: str | None,
        transaction: Transaction | None,
        op: typing.Callable[[sa_orm.Session], object],
    ) -> object:
        if transaction is not None:
            return op(transaction.session)
        with Transaction(self._adapter, instance_key) as tx:
            return op(tx.session)

    def _raise_integrity(self, exc: sa.exc.IntegrityError, mapping: ModelMapping) -> typing.NoReturn:
        message = str(exc.orig) if exc.orig is not None else str(exc)
        if "UNIQUE constraint failed" in message:
            observability.record_event(
                "constraint_violation", f"Unique constraint violated on {mapping.table_name}."
            )
            raise DuplicateRecordError(
                f"A {mapping.table_name} record with the same unique key already exists."
            ) from exc
        if "FOREIGN KEY constraint failed" in message:
            observability.record_event(
                "constraint_violation", f"Referential integrity violated on {mapping.table_name}."
            )
            raise ReferencedRecordMissingError(
                f"A referenced record does not exist for {mapping.table_name}."
            ) from exc
        observability.record_event(
            "constraint_violation", f"Unclassified integrity error on {mapping.table_name}."
        )
        raise

    def create(
        self,
        record: pydantic.BaseModel,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
    ) -> pydantic.BaseModel:
        model_cls = type(record)
        self._require_operation(model_cls, "create")
        table, mapping = self._mapping_for(model_cls)
        values = _to_storage_values(record, include_id=False)

        def _op(session: sa_orm.Session) -> pydantic.BaseModel:
            try:
                result = session.execute(sa.insert(table).values(**values))
                session.flush()
            except sa.exc.IntegrityError as exc:
                self._raise_integrity(exc, mapping)
            new_id = result.inserted_primary_key[0]
            return record.model_copy(update={"id": new_id})

        return self._run(instance_key, transaction, _op)  # type: ignore[return-value]

    def get_by_id(
        self,
        model_cls: ModelType,
        id: int,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
    ) -> pydantic.BaseModel | None:
        self._require_operation(model_cls, "get_by_id")
        table, _mapping = self._mapping_for(model_cls)

        def _op(session: sa_orm.Session) -> pydantic.BaseModel | None:
            row = session.execute(sa.select(table).where(table.c.id == id)).mappings().first()
            return None if row is None else _from_storage_row(row, model_cls)

        return self._run(instance_key, transaction, _op)  # type: ignore[return-value]

    def list(
        self,
        model_cls: ModelType,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
    ) -> list[pydantic.BaseModel]:
        self._require_operation(model_cls, "list")
        table, _mapping = self._mapping_for(model_cls)

        def _op(session: sa_orm.Session) -> list[pydantic.BaseModel]:
            rows = session.execute(sa.select(table)).mappings().all()
            return [_from_storage_row(row, model_cls) for row in rows]

        return self._run(instance_key, transaction, _op)  # type: ignore[return-value]

    def search(
        self,
        model_cls: ModelType,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
        **criteria: object,
    ) -> list[pydantic.BaseModel]:
        self._require_operation(model_cls, "search")
        table, _mapping = self._mapping_for(model_cls)

        def _op(session: sa_orm.Session) -> list[pydantic.BaseModel]:
            statement = sa.select(table)
            for field, value in criteria.items():
                statement = statement.where(table.c[field] == value)
            rows = session.execute(statement).mappings().all()
            return [_from_storage_row(row, model_cls) for row in rows]

        return self._run(instance_key, transaction, _op)  # type: ignore[return-value]

    def update(
        self,
        record: pydantic.BaseModel,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
    ) -> pydantic.BaseModel:
        model_cls = type(record)
        self._require_operation(model_cls, "update")
        table, mapping = self._mapping_for(model_cls)
        values = _to_storage_values(record, include_id=False)
        record_id = record.id  # type: ignore[attr-defined]

        def _op(session: sa_orm.Session) -> pydantic.BaseModel:
            try:
                result = session.execute(
                    sa.update(table).where(table.c.id == record_id).values(**values)
                )
            except sa.exc.IntegrityError as exc:
                self._raise_integrity(exc, mapping)
            if result.rowcount == 0:
                raise NotFoundError(f"No {model_cls.__name__} with id={record_id}.")
            return record

        return self._run(instance_key, transaction, _op)  # type: ignore[return-value]

    def delete(
        self,
        model_cls: ModelType,
        id: int,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
    ) -> None:
        self._require_operation(model_cls, "delete")
        table, mapping = self._mapping_for(model_cls)

        def _op(session: sa_orm.Session) -> None:
            try:
                result = session.execute(sa.delete(table).where(table.c.id == id))
            except sa.exc.IntegrityError as exc:
                self._raise_integrity(exc, mapping)
            if result.rowcount == 0:
                raise NotFoundError(f"No {model_cls.__name__} with id={id}.")

        self._run(instance_key, transaction, _op)

    def _set_active(
        self,
        model_cls: ModelType,
        id: int,
        active: bool,
        instance_key: str | None,
        transaction: Transaction | None,
    ) -> pydantic.BaseModel:
        operation = "enable" if active else "disable"
        self._require_operation(model_cls, operation)
        table, _mapping = self._mapping_for(model_cls)
        if "is_active" not in table.c:
            raise UnsupportedOperationError(f"{model_cls.__name__} has no is_active Field.")

        def _op(session: sa_orm.Session) -> pydantic.BaseModel:
            result = session.execute(
                sa.update(table).where(table.c.id == id).values(is_active=active)
            )
            if result.rowcount == 0:
                raise NotFoundError(f"No {model_cls.__name__} with id={id}.")
            row = session.execute(sa.select(table).where(table.c.id == id)).mappings().first()
            assert row is not None
            return _from_storage_row(row, model_cls)

        return self._run(instance_key, transaction, _op)  # type: ignore[return-value]

    def enable(
        self,
        model_cls: ModelType,
        id: int,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
    ) -> pydantic.BaseModel:
        return self._set_active(model_cls, id, True, instance_key, transaction)

    def disable(
        self,
        model_cls: ModelType,
        id: int,
        *,
        instance_key: str | None = None,
        transaction: Transaction | None = None,
    ) -> pydantic.BaseModel:
        return self._set_active(model_cls, id, False, instance_key, transaction)

    # <!-- Controlled command route (Database Principle 8) -->

    def execute_controlled_command(
        self, command: str, *, instance_key: str | None = None, **params: object
    ) -> object:
        """A capability-restricted, parameterized route for operations the standard pipeline
        cannot express. Structural changes, privilege changes, and Migration operations are
        never in the allow-list, so requesting one is rejected rather than performed."""
        handler = _CONTROLLED_COMMANDS.get(command)
        if handler is None:
            raise UnsupportedOperationError(
                f"'{command}' is not a permitted controlled command."
            )
        observability.record_event(
            "controlled_command",
            f"Executed controlled command '{command}' on Instance "
            f"'{instance_key or '<default>'}'.",
        )
        return handler(self, instance_key=instance_key, **params)

    def _reveal_credential(
        self, *, instance_key: str | None, model_cls: ModelType, id: int, field: str
    ) -> str | None:
        """Recover the plaintext of one `encrypted` credential Field. Reserved for the
        controlled-command route; never reachable through create/get_by_id/list/search/update
        (Database Principle 12)."""
        table, _mapping = self._mapping_for(model_cls)
        credential_storage = model_cls.credential_storage()
        if field not in credential_storage:
            raise UnsupportedOperationError(
                f"{model_cls.__name__}.{field} is not a declared credential Field."
            )
        mode = credential_storage[field]
        if mode != "encrypted":
            raise UnsupportedOperationError(
                f"{model_cls.__name__}.{field} uses '{mode}' at-rest treatment, "
                "which cannot be reversed."
            )

        def _op(session: sa_orm.Session) -> str | None:
            row = session.execute(
                sa.select(table.c[field]).where(table.c.id == id)
            ).first()
            if row is None:
                raise NotFoundError(f"No {model_cls.__name__} with id={id}.")
            stored = row[0]
            observability.record_event(
                "protected_data_access",
                f"Revealed credential Field '{field}' of {model_cls.__name__} id={id} "
                "(value not logged).",
            )
            return None if stored is None else decrypt_value(stored)

        return self._run(instance_key, None, _op)  # type: ignore[return-value]


_CONTROLLED_COMMANDS: dict[str, typing.Callable[..., object]] = {
    "reveal_credential": DatabaseInterface._reveal_credential,
}
