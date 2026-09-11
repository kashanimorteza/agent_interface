"""Database's public interface: the only boundary this package publishes.

A consumer supplies a Model type from the ``my_model`` package plus any
criteria an operation needs; the same generic pipeline serves every
persistent Model. No connection, mapping, or migration internal is exposed.
"""

from __future__ import annotations

from sqlalchemy import Connection

from . import _operations, _registry, _seed
from ._operations import RejectedOperationError, UnsupportedOperationError

__all__ = [
    "create",
    "get",
    "list",
    "update",
    "delete",
    "status",
    "transaction",
    "execute_sql",
    "list_instances",
    "default_instance",
    "seed_initial_data",
    "RejectedOperationError",
    "UnsupportedOperationError",
]


def create(model_cls, *, instance: str | None = None, conn: Connection | None = None, **values) -> dict:
    """Creates one record of ``model_cls``, validated by the Model, on the selected Instance."""
    return _operations.create(model_cls, instance=instance, conn=conn, **values)


def get(model_cls, id: int, *, instance: str | None = None, conn: Connection | None = None) -> dict | None:
    """Reads one record by id, or None. Credential fields are never included."""
    return _operations.get(model_cls, id, instance=instance, conn=conn)


def list(model_cls, *, instance: str | None = None, conn: Connection | None = None, **filters) -> list[dict]:
    """Lists records of ``model_cls`` matching the given field filters."""
    return _operations.list_(model_cls, instance=instance, conn=conn, **filters)


def update(model_cls, id: int, *, instance: str | None = None, conn: Connection | None = None, **values) -> dict:
    """Updates the given fields of one record; omitted fields are unchanged."""
    return _operations.update(model_cls, id, instance=instance, conn=conn, **values)


def delete(model_cls, id: int, *, instance: str | None = None, conn: Connection | None = None) -> bool:
    """Deletes one record by id. Returns whether a record was deleted."""
    return _operations.delete_(model_cls, id, instance=instance, conn=conn)


def status(model_cls, id: int, action: str, *, instance: str | None = None, conn: Connection | None = None) -> dict:
    """Enables or disables one record. Requires ``model_cls`` to declare a status field."""
    return _operations.status(model_cls, id, action, instance=instance, conn=conn)


def transaction(instance: str | None = None):
    """A context manager grouping related operations so they commit or roll back together.

    Usage: ``with database.transaction() as conn: database.create(X, conn=conn, ...)``.
    """
    return _operations.transaction(instance)


def execute_sql(sql: str, params: dict | None = None, *, instance: str | None = None, conn: Connection | None = None):
    """Executes one parameterized data command naming exactly one mapped table.

    Rejects structural changes and any command whose resulting data or
    protections cannot be established; see ``RejectedOperationError``.
    """
    return _operations.execute_sql(sql, params, instance=instance, conn=conn)


def list_instances() -> tuple:
    """Every configured Instance identity: key, name, and purpose."""
    return _registry.list_instances()


def default_instance():
    """The configured default Instance identity."""
    return _registry.default_instance()


def seed_initial_data(instance: str | None = None) -> dict[str, int]:
    """Seeds every Model's declared initial data. Repeatable without duplication."""
    return _seed.seed_all(instance)
