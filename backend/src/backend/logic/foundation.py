"""The Logic Foundation: standard Model operations shared by every Model Logic unit."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from database import ConstraintViolation
from pydantic import ValidationError

from ..database_interface import DatabaseInterface
from ..model_interface import ModelBase
from .outcomes import ConflictOutcome, NotFound, ValidationFailed


class ModelLogicBase[ModelT: ModelBase]:
    """Supplies create, read-by-identifier, list, search, update, delete, enable, and disable.

    `model_cls` is declared `ClassVar[type[ModelBase]]` rather than `type[ModelT]`
    because a ClassVar cannot reference its own class's type parameter; every concrete
    subclass sets it to the exact type `ModelT` is bound to, so the `cast` calls below
    describe a real, subclass-guaranteed invariant the type system cannot express.
    """

    model_cls: ClassVar[type[ModelBase]]

    def __init__(self, db: DatabaseInterface) -> None:
        self._db = db

    def create(self, data: dict[str, Any]) -> ModelT:
        try:
            instance = self.model_cls(**data)
        except ValidationError as exc:
            raise ValidationFailed(str(exc)) from exc
        try:
            return cast("ModelT", self._db.create(instance))
        except ConstraintViolation as exc:
            raise ConflictOutcome(str(exc)) from exc

    def get_by_id(self, id_: int) -> ModelT:
        result = self._db.get(self.model_cls, id_)
        if result is None:
            raise NotFound(self.model_cls.__name__, id_)
        return cast("ModelT", result)

    def list(self, **filters: Any) -> tuple[ModelT, ...]:
        return cast("tuple[ModelT, ...]", self._db.list(self.model_cls, **filters))

    def search(self, **filters: Any) -> tuple[ModelT, ...]:
        return self.list(**filters)

    def update(self, id_: int, data: dict[str, Any]) -> ModelT:
        existing = self.get_by_id(id_)
        merged = existing.model_dump()
        merged.update(data)
        merged["id"] = id_
        try:
            candidate = self.model_cls(**merged)
        except ValidationError as exc:
            raise ValidationFailed(str(exc)) from exc
        try:
            return cast("ModelT", self._db.update(candidate))
        except ConstraintViolation as exc:
            raise ConflictOutcome(str(exc)) from exc

    def enable(self, id_: int) -> ModelT:
        self.get_by_id(id_)
        return cast("ModelT", self._db.activate(self.model_cls, id_, enable=True))

    def disable(self, id_: int) -> ModelT:
        self.get_by_id(id_)
        return cast("ModelT", self._db.activate(self.model_cls, id_, enable=False))

    def delete(self, id_: int) -> None:
        self.get_by_id(id_)
        self._db.delete(self.model_cls, id_)
