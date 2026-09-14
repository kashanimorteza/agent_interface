"""The generic Database Interface: one Model-driven pipeline for every persisted Domain
Definition, an explicit Transaction boundary, and the capability-restricted controlled
command route."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

import model
from sqlalchemy.exc import IntegrityError

from . import commands, conversion, observability
from .adapter import StorageAdapter
from .exceptions import ConstraintViolation
from .mapping import MAPPING_REGISTRY
from .registry import InstanceRegistry
from .runtime_config import RuntimeConfig
from .transaction import Transaction, transaction

ModelT = TypeVar("ModelT", bound=model.ModelBase)


class Database:
    """The public, generic Database Interface."""

    def __init__(
        self,
        config: RuntimeConfig | None = None,
        *,
        instance: str | None = None,
        verify_schema: bool = True,
    ) -> None:
        self.adapter = StorageAdapter(config, instance=instance, verify_schema=verify_schema)
        self.instances = InstanceRegistry(self.adapter.config)

    @contextmanager
    def transaction(self) -> Iterator[Transaction]:
        with transaction(self.adapter) as txn:
            yield txn

    def _orm_class(self, model_cls: type[Any]) -> type[Any]:
        try:
            return MAPPING_REGISTRY[model_cls]
        except KeyError:
            raise ValueError(f"{model_cls.__name__} has no storage mapping") from None

    def _maybe_signal_access(self, model_cls: type[Any], operation: str) -> None:
        fields = conversion.credential_fields(model_cls)
        if fields:
            observability.protected_data_access(model_cls.__name__, fields, operation)

    def create(self, instance: Any, *, txn: Transaction | None = None) -> Any:
        model_cls = type(instance)
        orm_cls = self._orm_class(model_cls)

        def _do(session: Any) -> Any:
            kwargs = conversion.to_orm_kwargs(instance, db_instance_key=self.adapter.instance.key)
            kwargs.pop("id", None)
            row = orm_cls(**kwargs)
            session.add(row)
            try:
                session.flush()
            except IntegrityError as exc:
                observability.constraint_violation(model_cls.__name__, exc.__class__.__name__)
                raise ConstraintViolation(
                    f"{model_cls.__name__} violates a declared persistence constraint"
                ) from exc
            self._maybe_signal_access(model_cls, "create")
            return model_cls(**conversion.from_orm_kwargs(row, model_cls))

        return self._run(txn, _do)

    def get(
        self, model_cls: type[ModelT], id_: int, *, txn: Transaction | None = None
    ) -> ModelT | None:
        orm_cls = self._orm_class(model_cls)

        def _do(session: Any) -> ModelT | None:
            row = session.get(orm_cls, id_)
            if row is None:
                return None
            self._maybe_signal_access(model_cls, "read")
            return model_cls(**conversion.from_orm_kwargs(row, model_cls))

        return self._run(txn, _do)

    def list(
        self, model_cls: type[ModelT], *, txn: Transaction | None = None, **filters: Any
    ) -> tuple[ModelT, ...]:
        orm_cls = self._orm_class(model_cls)

        def _do(session: Any) -> tuple[ModelT, ...]:
            query = session.query(orm_cls)
            for field, value in filters.items():
                query = query.filter(getattr(orm_cls, field) == value)
            rows = query.all()
            if rows:
                self._maybe_signal_access(model_cls, "list")
            return tuple(model_cls(**conversion.from_orm_kwargs(row, model_cls)) for row in rows)

        return self._run(txn, _do)

    def update(self, instance: Any, *, txn: Transaction | None = None) -> Any:
        model_cls = type(instance)
        orm_cls = self._orm_class(model_cls)
        credential_fields = conversion.credential_fields(model_cls)

        def _do(session: Any) -> Any:
            row = session.get(orm_cls, instance.id)
            if row is None:
                raise ValueError(f"No {model_cls.__name__} with id={instance.id} to update")
            data = instance.model_dump()
            for field, value in data.items():
                if field == "id":
                    continue
                if field in credential_fields:
                    if value is None or value == conversion.REDACTED:
                        continue  # unchanged credential: never overwrite with a redacted echo
                    from . import credentials

                    value = credentials.protect(
                        value,
                        model_name=model_cls.__name__,
                        field_name=field,
                        instance=self.adapter.instance.key,
                    )
                setattr(row, field, value)
            try:
                session.flush()
            except IntegrityError as exc:
                observability.constraint_violation(model_cls.__name__, exc.__class__.__name__)
                raise ConstraintViolation(
                    f"{model_cls.__name__} violates a declared persistence constraint"
                ) from exc
            self._maybe_signal_access(model_cls, "update")
            return model_cls(**conversion.from_orm_kwargs(row, model_cls))

        return self._run(txn, _do)

    def delete(self, model_cls: type[Any], id_: int, *, txn: Transaction | None = None) -> None:
        orm_cls = self._orm_class(model_cls)

        def _do(session: Any) -> None:
            row = session.get(orm_cls, id_)
            if row is None:
                return
            session.delete(row)
            try:
                session.flush()
            except IntegrityError as exc:
                observability.constraint_violation(model_cls.__name__, exc.__class__.__name__)
                raise ConstraintViolation(
                    f"{model_cls.__name__} cannot be deleted: a referencing record exists"
                ) from exc

        self._run(txn, _do)

    def activate(
        self, model_cls: type[ModelT], id_: int, *, enable: bool, txn: Transaction | None = None
    ) -> ModelT:
        if "is_active" not in model_cls.model_fields:
            raise ValueError(f"{model_cls.__name__} declares no is_active field to activate")
        orm_cls = self._orm_class(model_cls)

        def _do(session: Any) -> ModelT:
            row = session.get(orm_cls, id_)
            if row is None:
                raise ValueError(f"No {model_cls.__name__} with id={id_} to activate")
            row.is_active = enable
            session.flush()
            return model_cls(**conversion.from_orm_kwargs(row, model_cls))

        return self._run(txn, _do)

    def execute_command(self, name: str, *, txn: Transaction | None = None, **params: Any) -> Any:
        """Execute one allow-listed controlled command through the controlled command route."""
        if txn is not None:
            return commands.execute_command(txn, name, **params)
        with self.transaction() as own_txn:
            return commands.execute_command(own_txn, name, **params)

    def _run(self, txn: Transaction | None, action: Any) -> Any:
        if txn is not None:
            return action(txn.session)
        with self.transaction() as own_txn:
            return action(own_txn.session)
