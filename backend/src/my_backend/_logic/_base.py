from __future__ import annotations

from typing import ClassVar, Generic, Literal, TypeVar

from my_model import DomainModel

from .._data_access import DataAccess, data_access

M = TypeVar("M", bound=DomainModel)


class ModelLogic(Generic[M]):
    model_cls: ClassVar[type[DomainModel]]

    def __init__(self, access: DataAccess | None = None) -> None:
        self._access = access or data_access

    def create(self, data: dict) -> DomainModel:
        return self._access.create(self.model_cls, data)

    def get(self, id_: int) -> DomainModel | None:
        return self._access.get(self.model_cls, id_)

    def list(self, *, where: dict | None = None) -> list[DomainModel]:
        return self._access.list(self.model_cls, where=where)

    def update(self, id_: int, data: dict) -> DomainModel:
        return self._access.update(self.model_cls, id_, data)

    def delete(self, id_: int) -> bool:
        return self._access.delete(self.model_cls, id_)

    def set_status(self, id_: int, action: Literal["enable", "disable"]) -> DomainModel:
        if "status" not in self.model_cls.model_fields:
            raise TypeError(f"{self.model_cls.__name__} does not declare a status field.")
        return self._access.set_status(self.model_cls, id_, action)
