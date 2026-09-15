"""The generic, Model-driven Database Interface — Database's one public boundary.

Accepts a public Model type or instance, a supported operation, and that
operation's criteria, and performs create, read, read-by-identifier, list,
search, update, delete, and activation against the mapped storage structure
for any persistent Domain Definition through one pipeline. No Model name is
ever encoded as an untyped string; identity is always carried by the
imported Domain Definition type or instance.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any, TypeVar

from model import ModelBase
from sqlalchemy import Table, delete, func, insert, select, update
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from database import credentials, observability
from database.adapter import StorageAdapter
from database.mapping import MODEL_KEYS, model_key, table_name

M = TypeVar("M", bound=ModelBase)

_ALLOWED_CONTROLLED_COMMANDS = frozenset({"count"})


class UnknownDomainDefinitionError(LookupError):
    """Raised when a Model type has no registered persistence mapping."""


class RecordNotFoundError(LookupError):
    """Raised when a read-by-identifier, update, or delete target does not exist."""


class ActivationNotSupportedError(ValueError):
    """Raised when activation is requested for a Domain Definition without an is_active field."""


class UnknownSearchFieldError(ValueError):
    """Raised when search or a controlled command names a field the Domain Definition does not declare."""


class UnknownControlledCommandError(LookupError):
    """Raised when an unrecognized, non-allow-listed controlled command is requested."""


def _table_for(adapter: StorageAdapter, model_cls: type[ModelBase]) -> Table:
    key = model_key(model_cls)
    if key not in MODEL_KEYS:
        raise UnknownDomainDefinitionError(model_cls.__name__)
    return adapter.metadata.tables[table_name(model_cls)]


def _credential_fields(model_cls: type[ModelBase]) -> dict[str, str]:
    contract = model_cls.persistence_contract()
    return {
        name: meta["credential"]
        for name, meta in contract["fields"].items()
        if "credential" in meta
    }


def _apply_credentials(
    model_cls: type[ModelBase], data: dict[str, Any]
) -> dict[str, Any]:
    protected = dict(data)
    for field, treatment in _credential_fields(model_cls).items():
        if field in protected and protected[field] is not None:
            protected[field] = credentials.apply_at_rest_treatment(
                treatment, protected[field]
            )
    return protected


class Transaction:
    """One atomic unit of grouped operations on a single Instance's connection."""

    def __init__(self, connection: Connection, instance_key: str) -> None:
        self.connection = connection
        self.instance_key = instance_key


class DatabaseInterface:
    """The one generic, Model-driven public Database boundary."""

    def __init__(self, adapter: StorageAdapter | None = None) -> None:
        self._adapter = adapter or StorageAdapter()

    @property
    def adapter(self) -> StorageAdapter:
        return self._adapter

    @contextmanager
    def transaction(self, instance_key: str | None = None) -> Iterator[Transaction]:
        """Group related operations on one Instance into one atomic commit/rollback unit."""
        resolved = self._adapter.resolve_instance(instance_key)
        engine = self._adapter.engine_for(resolved.key)
        connection = engine.connect()
        txn = connection.begin()
        try:
            yield Transaction(connection, resolved.key)
        except IntegrityError as error:
            txn.rollback()
            observability.record_constraint_violation("unknown", error)
            raise
        except Exception as error:
            txn.rollback()
            observability.record_transaction_conflict(resolved.key, error)
            raise
        else:
            txn.commit()
        finally:
            connection.close()

    @contextmanager
    def _connection(
        self, instance_key: str | None, txn: Transaction | None
    ) -> Iterator[Connection]:
        """Yield a connection: the grouped Transaction's own connection, or a standalone atomic unit."""
        if txn is not None:
            yield txn.connection
            return
        resolved = self._adapter.resolve_instance(instance_key)
        engine = self._adapter.engine_for(resolved.key)
        with engine.begin() as connection:
            yield connection

    def create(
        self,
        instance: M,
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> M:
        """Create one record from a Domain Definition instance, applying every declared credential treatment.

        Model's `id` Field carries no absence state of its own (Model
        Principle 6), so the caller supplies any placeholder value; an
        auto-increment primary key is always assigned by storage and never
        trusted from that placeholder, and the returned instance carries the
        real, storage-assigned value.
        """
        model_cls = type(instance)
        table = _table_for(self._adapter, model_cls)
        data = _apply_credentials(model_cls, instance.model_dump())
        pk_column = next(iter(table.primary_key.columns))
        if pk_column.autoincrement is True:
            data.pop(pk_column.name, None)
        with self._connection(instance_key, txn) as connection:
            try:
                result = connection.execute(insert(table).values(**data))
            except IntegrityError as error:
                observability.record_constraint_violation(table.name, error)
                raise
            if pk_column.autoincrement is True:
                inserted_pk = result.inserted_primary_key
                assert inserted_pk is not None
                data[pk_column.name] = inserted_pk[0]
        return model_cls.model_validate(data)

    def get_by_id(
        self,
        model_cls: type[M],
        identifier: Any,
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> M | None:
        """Read one record by its primary identifier; None when it does not exist."""
        table = _table_for(self._adapter, model_cls)
        pk_column = next(iter(table.primary_key.columns))
        with self._connection(instance_key, txn) as connection:
            row = (
                connection.execute(select(table).where(pk_column == identifier))
                .mappings()
                .first()
            )
        return model_cls.model_validate(dict(row)) if row is not None else None

    def list(
        self,
        model_cls: type[M],
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> list[M]:
        """List every record of a persistent Domain Definition."""
        table = _table_for(self._adapter, model_cls)
        with self._connection(instance_key, txn) as connection:
            rows = connection.execute(select(table)).mappings().all()
        return [model_cls.model_validate(dict(row)) for row in rows]

    def search(
        self,
        model_cls: type[M],
        criteria: Mapping[str, Any],
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> list[M]:
        """List every record matching an equality filter over one or more declared fields."""
        table = _table_for(self._adapter, model_cls)
        for field in criteria:
            if field not in table.columns:
                raise UnknownSearchFieldError(
                    f"{model_cls.__name__} has no searchable field '{field}'"
                )
        stmt = select(table)
        for field, value in criteria.items():
            stmt = stmt.where(table.columns[field] == value)
        with self._connection(instance_key, txn) as connection:
            rows = connection.execute(stmt).mappings().all()
        return [model_cls.model_validate(dict(row)) for row in rows]

    def update(
        self,
        model_cls: type[M],
        identifier: Any,
        changes: Mapping[str, Any],
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> M:
        """Update the named fields of one record, applying credential treatment to any credential field provided."""
        table = _table_for(self._adapter, model_cls)
        pk_column = next(iter(table.primary_key.columns))
        protected_changes = _apply_credentials(model_cls, dict(changes))
        with self._connection(instance_key, txn) as connection:
            try:
                result = connection.execute(
                    update(table)
                    .where(pk_column == identifier)
                    .values(**protected_changes)
                )
            except IntegrityError as error:
                observability.record_constraint_violation(table.name, error)
                raise
            if result.rowcount == 0:
                raise RecordNotFoundError(f"{model_cls.__name__}[{identifier}]")
            row = (
                connection.execute(select(table).where(pk_column == identifier))
                .mappings()
                .first()
            )
            if row is None:
                raise RecordNotFoundError(f"{model_cls.__name__}[{identifier}]")
        return model_cls.model_validate(dict(row))

    def delete(
        self,
        model_cls: type[M],
        identifier: Any,
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> None:
        """Delete one record by its primary identifier."""
        table = _table_for(self._adapter, model_cls)
        pk_column = next(iter(table.primary_key.columns))
        with self._connection(instance_key, txn) as connection:
            try:
                result = connection.execute(
                    delete(table).where(pk_column == identifier)
                )
            except IntegrityError as error:
                observability.record_constraint_violation(table.name, error)
                raise
            if result.rowcount == 0:
                raise RecordNotFoundError(f"{model_cls.__name__}[{identifier}]")

    def set_active(
        self,
        model_cls: type[M],
        identifier: Any,
        active: bool,
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> M:
        """Enable (True) or disable (False) one record; only for a Domain Definition that declares is_active."""
        table = _table_for(self._adapter, model_cls)
        if "is_active" not in table.columns:
            raise ActivationNotSupportedError(model_cls.__name__)
        return self.update(
            model_cls,
            identifier,
            {"is_active": active},
            instance_key=instance_key,
            txn=txn,
        )

    def enable(
        self,
        model_cls: type[M],
        identifier: Any,
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> M:
        return self.set_active(
            model_cls, identifier, True, instance_key=instance_key, txn=txn
        )

    def disable(
        self,
        model_cls: type[M],
        identifier: Any,
        *,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> M:
        return self.set_active(
            model_cls, identifier, False, instance_key=instance_key, txn=txn
        )

    def execute_command(
        self,
        name: str,
        *,
        model_cls: type[ModelBase],
        criteria: Mapping[str, Any] | None = None,
        instance_key: str | None = None,
        txn: Transaction | None = None,
    ) -> Any:
        """Execute one explicit, parameterized, allow-listed controlled command.

        Every command is named and typed in advance; an unrecognized name is
        rejected rather than interpreted, so this route can never perform a
        structural change, a privilege change, connection administration, or
        a Migration operation — none of those is, or ever will be, an
        allow-listed command name.
        """
        if name not in _ALLOWED_CONTROLLED_COMMANDS:
            raise UnknownControlledCommandError(name)
        table = _table_for(self._adapter, model_cls)
        criteria = criteria or {}
        for field in criteria:
            if field not in table.columns:
                raise UnknownSearchFieldError(
                    f"{model_cls.__name__} has no field '{field}'"
                )
        stmt = select(func.count()).select_from(table)
        for field, value in criteria.items():
            stmt = stmt.where(table.columns[field] == value)
        with self._connection(instance_key, txn) as connection:
            result = connection.execute(stmt).scalar_one()
        observability.record_controlled_command(name, table.name)
        return result
