"""The published transaction boundary.

A consumer groups related operations on one Instance. The group's changes
are committed together only when the whole unit succeeds, and are undone
together when it fails or is cancelled. No operation inside the group is
durable before the group completes, and the connection behind it is never
handed over.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from my_model import Model
from sqlalchemy import Connection

from ..errors import DatabaseError
from ..logic.operations import Pipeline

COMMITTED = "committed"
ROLLED_BACK = "rolled back"
RUNNING = "running"


class TransactionCancelled(DatabaseError):
    """Raised inside a group by ``cancel`` and absorbed by the boundary."""


class Transaction:
    """One unit of data operations on a single Instance.

    It offers the same operations as the gateway; every one of them runs on
    this unit's connection and none of them commits on its own.
    """

    def __init__(self, pipeline: Pipeline, connection: Connection, instance_key: str) -> None:
        self._pipeline = pipeline
        self._connection = connection
        self._instance = instance_key
        self.outcome: str = RUNNING

    @property
    def instance(self) -> str:
        """The one Instance this unit acts on."""
        return self._instance

    # -- operations, all bound to this unit ----------------------------------

    def create(self, model: type[Model] | Model, data: Mapping[str, Any] | None = None) -> Model:
        return self._pipeline.create(model, data, self._instance, self._connection)

    def read(self, model: type[Model] | Model, key: Any) -> Model:
        return self._pipeline.read(model, key, self._instance, self._connection)

    def list(self, model: type[Model] | Model, criteria: Mapping[str, Any] | None = None) -> list[Model]:
        return self._pipeline.list(model, criteria, self._instance, self._connection)

    def update(self, model: type[Model] | Model, key: Any, changes: Mapping[str, Any]) -> Model:
        return self._pipeline.update(model, key, changes, self._instance, self._connection)

    def delete(self, model: type[Model] | Model, key: Any) -> None:
        self._pipeline.delete(model, key, self._instance, self._connection)

    def status(self, model: type[Model] | Model, key: Any, action: str) -> Model:
        return self._pipeline.status(model, key, action, self._instance, self._connection)

    def execute(self, statement: str, parameters: Mapping[str, Any] | None = None, *,
                engine: str | None = None) -> list[dict[str, Any]]:
        return self._pipeline.execute(statement, parameters, engine, self._instance, self._connection)

    def verify_credential(self, model: type[Model] | Model, key: Any, field: str, given: str) -> bool:
        return self._pipeline.verify_credential(model, key, field, given, self._instance, self._connection)

    def recover_credential(self, model: type[Model] | Model, key: Any, field: str) -> str:
        return self._pipeline.recover_credential(model, key, field, self._instance, self._connection)

    # -- control -------------------------------------------------------------

    def cancel(self) -> None:
        """End the unit without keeping any of its changes."""
        raise TransactionCancelled(f"the unit on Instance {self._instance!r} was cancelled")
