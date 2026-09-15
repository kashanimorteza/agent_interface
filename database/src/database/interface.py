"""The Database Interface: one generic, Model-driven pipeline for every persistent Model.

Every public operation accepts a public Model type or instance, never an
untyped Model-name string, and there is exactly one implementation of each
operation shared by every Model.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

from model.foundation import DomainModel
from sqlalchemy import delete as sa_delete
from sqlalchemy import insert, select
from sqlalchemy import update as sa_update
from sqlalchemy.engine import Connection

from database.adapter import get_engine
from database.credentials import apply_treatment
from database.mapping import build_all_tables, table_for

build_all_tables()


class NotPersistentError(Exception):
    """Raised when an operation targets a Model that declares no persistence."""


class RecordNotFoundError(Exception):
    """Raised when a lookup by identifier finds no matching record."""


class UnsupportedOperationError(Exception):
    """Raised for an operation a Model does not support, or an unlisted controlled command."""


def _credential_fields(model_cls: type[DomainModel]) -> dict[str, str]:
    fields = model_cls.persistence_metadata()["fields"]
    return {
        name: meta["credential"] for name, meta in fields.items() if meta["credential"]
    }


def _row_to_model[M: DomainModel](model_cls: type[M], row: Any) -> M:
    return model_cls(**dict(row._mapping))


def _values_for_create(instance: DomainModel) -> dict[str, Any]:
    """Apply declared at-rest treatment to every classified credential's raw input value."""
    data = instance.model_dump(mode="json")
    for field, classification in _credential_fields(type(instance)).items():
        if data.get(field) is not None:
            data[field] = apply_treatment(classification, data[field])
    return data


def _values_for_update(instance: DomainModel) -> dict[str, Any]:
    """Exclude credential fields: an already-persisted value is already transformed,

    and a caller reads it back transformed too, so re-applying treatment on update
    would corrupt it (double-hashing a hash, or re-encrypting a ciphertext).
    Credential rotation is a distinct capability outside this generic operation.
    """
    data = instance.model_dump(mode="json")
    for field in _credential_fields(type(instance)):
        data.pop(field, None)
    return data


class DatabaseSession:
    """Bound to one open Transaction; every method participates in that same unit."""

    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def create[M: DomainModel](self, instance: M) -> M:
        model_cls = type(instance)
        table = table_for(model_cls)
        if table is None:
            raise NotPersistentError(model_cls)
        values = _values_for_create(instance)
        result = self._conn.execute(insert(table).values(**values))
        new_id = result.inserted_primary_key[0]  # type: ignore[index]
        return self.get_by_id(model_cls, new_id)

    def get_by_id[M: DomainModel](self, model_cls: type[M], id_: int) -> M:
        table = table_for(model_cls)
        if table is None:
            raise NotPersistentError(model_cls)
        row = self._conn.execute(select(table).where(table.c.id == id_)).first()
        if row is None:
            raise RecordNotFoundError(model_cls, id_)
        return _row_to_model(model_cls, row)

    def list[M: DomainModel](
        self, model_cls: type[M], *, limit: int = 50, offset: int = 0
    ) -> list[M]:
        table = table_for(model_cls)
        if table is None:
            raise NotPersistentError(model_cls)
        rows = self._conn.execute(select(table).limit(limit).offset(offset)).all()
        return [_row_to_model(model_cls, row) for row in rows]

    def search[M: DomainModel](self, model_cls: type[M], **criteria: Any) -> list[M]:
        table = table_for(model_cls)
        if table is None:
            raise NotPersistentError(model_cls)
        statement = select(table)
        for field, value in criteria.items():
            statement = statement.where(getattr(table.c, field) == value)
        rows = self._conn.execute(statement).all()
        return [_row_to_model(model_cls, row) for row in rows]

    def update[M: DomainModel](self, instance: M) -> M:
        model_cls = type(instance)
        table = table_for(model_cls)
        if table is None:
            raise NotPersistentError(model_cls)
        values = _values_for_update(instance)
        record_id = values.pop("id")
        self._conn.execute(
            sa_update(table).where(table.c.id == record_id).values(**values)
        )
        return self.get_by_id(model_cls, record_id)

    def delete(self, model_cls: type[DomainModel], id_: int) -> None:
        table = table_for(model_cls)
        if table is None:
            raise NotPersistentError(model_cls)
        self._conn.execute(sa_delete(table).where(table.c.id == id_))

    def set_active[M: DomainModel](
        self, model_cls: type[M], id_: int, *, active: bool
    ) -> M:
        if "is_active" not in model_cls.model_fields:
            raise UnsupportedOperationError(
                f"{model_cls.__name__} does not declare is_active"
            )
        table = table_for(model_cls)
        if table is None:
            raise NotPersistentError(model_cls)
        self._conn.execute(
            sa_update(table).where(table.c.id == id_).values(is_active=active)
        )
        return self.get_by_id(model_cls, id_)

    def execute_command(self, name: str, **params: Any) -> Any:
        try:
            command = _CONTROLLED_COMMANDS[name]
        except KeyError:
            raise UnsupportedOperationError(
                f"Unknown controlled command: {name}"
            ) from None
        return command(self, **params)


def _cmd_increment_account_balance(
    session: DatabaseSession, *, account_id: int, delta: Any
) -> Any:
    """Adjust an Account's balance by `delta` — not expressible through standard update alone."""
    from model import Account

    table = table_for(Account)
    assert table is not None
    session._conn.execute(
        sa_update(table)
        .where(table.c.id == account_id)
        .values(balance=table.c.balance + delta)
    )
    return session.get_by_id(Account, account_id)


_CONTROLLED_COMMANDS: dict[str, Callable[..., Any]] = {
    "increment_account_balance": _cmd_increment_account_balance,
}


@contextmanager
def transaction(instance_key: str | None = None) -> Iterator[DatabaseSession]:
    """Group related operations on one Instance into one atomic commit-or-rollback unit."""
    engine = get_engine(instance_key)
    with engine.begin() as connection:
        yield DatabaseSession(connection)


def create[M: DomainModel](instance: M, *, instance_key: str | None = None) -> M:
    with transaction(instance_key) as session:
        return session.create(instance)


def get_by_id[M: DomainModel](
    model_cls: type[M], id_: int, *, instance_key: str | None = None
) -> M:
    with transaction(instance_key) as session:
        return session.get_by_id(model_cls, id_)


def list_[M: DomainModel](
    model_cls: type[M],
    *,
    limit: int = 50,
    offset: int = 0,
    instance_key: str | None = None,
) -> list[M]:
    with transaction(instance_key) as session:
        return session.list(model_cls, limit=limit, offset=offset)


def search[M: DomainModel](
    model_cls: type[M], *, instance_key: str | None = None, **criteria: Any
) -> list[M]:
    with transaction(instance_key) as session:
        return session.search(model_cls, **criteria)


def update[M: DomainModel](instance: M, *, instance_key: str | None = None) -> M:
    with transaction(instance_key) as session:
        return session.update(instance)


def delete(
    model_cls: type[DomainModel], id_: int, *, instance_key: str | None = None
) -> None:
    with transaction(instance_key) as session:
        session.delete(model_cls, id_)


def set_active[M: DomainModel](
    model_cls: type[M], id_: int, *, active: bool, instance_key: str | None = None
) -> M:
    with transaction(instance_key) as session:
        return session.set_active(model_cls, id_, active=active)


def execute_command(
    name: str, *, instance_key: str | None = None, **params: Any
) -> Any:
    with transaction(instance_key) as session:
        return session.execute_command(name, **params)
