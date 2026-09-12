"""Shared Logic baseline reused by every Model's own Logic unit.

Each Model still gets its own Logic unit (its own subclass, in its own
module); this shared base only supplies the common create/get/list/update/
delete/status baseline through inheritance, per Backend Standard 2.5.
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from my_model._base import BaseModel

from my_backend import _database_interface as db


class ModelLogic[T: BaseModel]:
    model_cls: ClassVar[type[BaseModel]]

    @classmethod
    def create(cls, data: dict[str, Any]) -> T:
        record = cls.model_cls(**data)
        return db.create(record)  # type: ignore[return-value]

    @classmethod
    def get(cls, record_id: int) -> T | None:
        return db.get(cls.model_cls, record_id)  # type: ignore[return-value]

    @classmethod
    def list(
        cls, *, limit: int | None = None, offset: int | None = None, **filters: Any
    ) -> list[T]:
        return db.list_(cls.model_cls, limit=limit, offset=offset, **filters)  # type: ignore[return-value]

    @classmethod
    def update(cls, record_id: int, changes: dict[str, Any]) -> T:
        return db.update(cls.model_cls, record_id, **changes)  # type: ignore[return-value]

    @classmethod
    def delete(cls, record_id: int) -> bool:
        return db.delete(cls.model_cls, record_id)

    @classmethod
    def set_status(cls, record_id: int, action: Literal["enable", "disable"]) -> T:
        return db.set_status(cls.model_cls, record_id, action)  # type: ignore[return-value]
