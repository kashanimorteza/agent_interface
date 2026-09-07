"""The Model-driven operation pipeline.

One generic implementation serves every persistent Model: differences come
from the Model's resolved fields, relationships, constraints, credential modes,
and storage mapping. Credential values are transformed on write and never
populated on returned instances.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ValidationError

from ..errors import NotFoundError, OperationError
from ..storage_adapter import Storage
from . import credentials
from .mapping import PRIMARY_KEY, STATUS_FIELD, Mapped, mapped

STATUS_ACTIONS = {"enable": True, "disable": False}


class Operations:
    def __init__(self, storage: Storage, key: credentials.KeyProvider) -> None:
        self._storage = storage
        self._key = key

    # ---------------------------------------------------------------- standard operations
    def create(self, instance: BaseModel) -> BaseModel:
        m = self._mapped_instance(instance)
        row = instance.model_dump(exclude={PRIMARY_KEY})
        for field_name, mode in m.credentials.items():
            if row.get(field_name) is None:
                raise OperationError(f"{m.model.__name__}.{field_name} is a credential and must be supplied on create")
            row[field_name] = credentials.transform(mode, row[field_name], self._key)
        key = self._storage.insert(m.table, row)
        return self._require(m, key)

    def read(self, model: type, key: int) -> BaseModel | None:
        m = self._mapped_type(model)
        row = self._storage.select_one(m.table, self._key_of(key))
        return None if row is None else self._to_model(m, row)

    def list(
        self,
        model: type,
        criteria: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[BaseModel]:
        m = self._mapped_type(model)
        criteria = dict(criteria or {})
        for field_name in criteria:
            self._require_field(m, field_name, "criteria")
        if any(field_name in m.credentials for field_name in criteria):
            raise OperationError("a credential field cannot be used as a criterion")
        order = order_by or PRIMARY_KEY
        self._require_field(m, order, "order_by")
        for name, value in (("limit", limit), ("offset", offset)):
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                raise OperationError(f"{name} must be a non-negative integer")
        rows = self._storage.select_many(m.table, criteria, order, limit, offset)
        return [self._to_model(m, row) for row in rows]

    def update(self, instance: BaseModel) -> BaseModel:
        m = self._mapped_instance(instance)
        key = getattr(instance, PRIMARY_KEY, None)
        if key is None:
            raise OperationError(f"update requires the {m.model.__name__} instance to carry its primary key")
        values = instance.model_dump(exclude={PRIMARY_KEY})
        for field_name, mode in m.credentials.items():
            if values.get(field_name) is None:
                values.pop(field_name, None)  # an absent credential leaves the stored one untouched
            else:
                values[field_name] = credentials.transform(mode, values[field_name], self._key)
        if self._storage.update(m.table, self._key_of(key), values) == 0:
            raise NotFoundError(f"{m.model.__name__} {key} does not exist")
        return self._require(m, key)

    def delete(self, model: type, key: int) -> None:
        m = self._mapped_type(model)
        if self._storage.delete(m.table, self._key_of(key)) == 0:
            raise NotFoundError(f"{m.model.__name__} {key} does not exist")

    def status(self, model: type, key: int, action: str) -> BaseModel:
        m = self._mapped_type(model)
        if not m.has_status:
            raise OperationError(f"{m.model.__name__} declares no {STATUS_FIELD} field")
        if action not in STATUS_ACTIONS:
            raise OperationError(f"status accepts exactly {' or '.join(STATUS_ACTIONS)}, not {action!r}")
        if self._storage.update(m.table, self._key_of(key), {STATUS_FIELD: STATUS_ACTIONS[action]}) == 0:
            raise NotFoundError(f"{m.model.__name__} {key} does not exist")
        return self._require(m, key)

    def sql(self, statement: str, parameters: dict[str, Any] | None = None) -> list[tuple[Any, ...]]:
        if not isinstance(statement, str) or not statement.strip():
            raise OperationError("sql requires a non-empty statement")
        if parameters is not None and not isinstance(parameters, dict):
            raise OperationError("sql parameters must be a mapping of placeholder name to value")
        return self._storage.execute(statement, parameters)

    # ---------------------------------------------------------------- pipeline helpers
    @staticmethod
    def _mapped_type(model: type) -> Mapped:
        if not isinstance(model, type):
            raise OperationError("a Model class exported by my_model is required; an untyped Model selector is not accepted")
        try:
            return mapped(model)
        except LookupError as error:
            raise OperationError(str(error)) from None

    @staticmethod
    def _mapped_instance(instance: BaseModel) -> Mapped:
        if not isinstance(instance, BaseModel):
            raise OperationError("a Model instance exported by my_model is required")
        try:
            return mapped(type(instance))
        except LookupError as error:
            raise OperationError(str(error)) from None

    @staticmethod
    def _key_of(key: Any) -> int:
        if isinstance(key, bool) or not isinstance(key, int):
            raise OperationError("the primary key must be an integer")
        return key

    @staticmethod
    def _require_field(m: Mapped, field_name: str, where: str) -> None:
        if field_name not in m.fields:
            raise OperationError(f"{where}: {m.model.__name__} has no field {field_name!r}")

    def _require(self, m: Mapped, key: int) -> BaseModel:
        row = self._storage.select_one(m.table, key)
        if row is None:
            raise NotFoundError(f"{m.model.__name__} {key} does not exist")
        return self._to_model(m, row)

    @staticmethod
    def _to_model(m: Mapped, row: dict[str, Any]) -> BaseModel:
        values = {k: v for k, v in row.items() if k in m.fields}
        for field_name in m.credentials:
            values[field_name] = None
        try:
            return m.model.model_validate(values)
        except ValidationError as error:
            raise OperationError(f"stored {m.model.__name__} {row.get(PRIMARY_KEY)} does not satisfy the Model: {error}") from None
