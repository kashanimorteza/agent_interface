"""The Database gateway: the only boundary consumers use."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from ..data_logic import Operations
from ..errors import UnknownInstanceError
from ..storage_adapter import Storage, credential_key, load_settings, make_engine
from .registry import InstanceIdentity, InstanceRegistry


class Database:
    """Generic Model operations against one Instance.

    ``Database()`` selects the default Instance and ``Database(instance=<key>)``
    a named one. Construction resolves the settings and binds the Engine but
    opens no connection; the Instance's file is touched by the first operation.
    """

    def __init__(self, instance: str | None = None) -> None:
        settings = load_settings()
        registry = InstanceRegistry(settings)
        key = (instance or registry.default).strip().lower()
        if key not in settings.instances:
            raise UnknownInstanceError(
                f"Instance {key!r} is not configured; configured Instances: {', '.join(settings.instances)}"
            )
        self._identity = registry.get(key)
        self._operations = Operations(Storage(make_engine(settings.instances[key])), credential_key)

    @property
    def instance(self) -> InstanceIdentity:
        """The identity of the selected Instance."""
        return self._identity

    def create(self, instance: BaseModel) -> BaseModel:
        return self._operations.create(instance)

    def read(self, model: type, key: int) -> BaseModel | None:
        return self._operations.read(model, key)

    def list(
        self,
        model: type,
        criteria: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[BaseModel]:
        return self._operations.list(model, criteria, order_by, limit, offset)

    def update(self, instance: BaseModel) -> BaseModel:
        return self._operations.update(instance)

    def delete(self, model: type, key: int) -> None:
        self._operations.delete(model, key)

    def status(self, model: type, key: int, action: str) -> BaseModel:
        return self._operations.status(model, key, action)

    def sql(self, statement: str, parameters: dict[str, Any] | None = None) -> list[tuple[Any, ...]]:
        return self._operations.sql(statement, parameters)

    def __repr__(self) -> str:
        return f"Database(instance={self._identity.key!r})"
