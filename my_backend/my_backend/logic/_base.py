"""The generic Model Logic base every distinct Model Logic unit extends.

Backend Principle 4 permits shared Behaviour through a common base; each
concrete unit below still has its own separate identity and may extend or
override any operation with Model-specific Behaviour.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal

from my_backend import _database_interface as db
from my_backend._model_interface import BaseModel as ModelBaseModel


class ModelLogic[T: ModelBaseModel]:
    """Offers the standard operations every Model with a status field
    supports: create, get, list, update, delete, and status.
    """

    def __init__(self, model_type: type[T]) -> None:
        self.model_type = model_type

    def create(self, data: dict[str, Any]) -> T:
        record = self.model_type(id=0, **data)  # pyright: ignore[reportCallIssue]
        return db.create(record)

    def get(self, id: int) -> T:
        return db.get(self.model_type, id)

    def list(self, *, limit: int = 50, offset: int = 0) -> Sequence[T]:
        return db.list_all(self.model_type, limit=limit, offset=offset)

    def update(self, id: int, patch: dict[str, Any]) -> T:
        return db.update(self.model_type, id, patch)

    def delete(self, id: int) -> None:
        db.remove(self.model_type, id)

    def set_status(self, id: int, action: Literal["enable", "disable"]) -> T:
        return db.set_status(self.model_type, id, action)
