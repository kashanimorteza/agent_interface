from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Literal, Union

import my_database as db
from my_model import DomainModel


class DataAccess:
    def __init__(self, gateway: Union["db.Database", "db.BoundDatabase", None] = None) -> None:
        self._gateway = gateway if gateway is not None else db.gateway

    def create(self, model_cls: type[DomainModel], data: dict) -> DomainModel:
        return self._gateway.create(model_cls, data)

    def get(self, model_cls: type[DomainModel], id_: int) -> DomainModel | None:
        return self._gateway.get(model_cls, id_)

    def list(self, model_cls: type[DomainModel], *, where: dict | None = None) -> list[DomainModel]:
        return self._gateway.list(model_cls, where=where)

    def update(self, model_cls: type[DomainModel], id_: int, data: dict) -> DomainModel:
        return self._gateway.update(model_cls, id_, data)

    def delete(self, model_cls: type[DomainModel], id_: int) -> bool:
        return self._gateway.delete(model_cls, id_)

    def set_status(
        self, model_cls: type[DomainModel], id_: int, action: Literal["enable", "disable"]
    ) -> DomainModel:
        return self._gateway.set_status(model_cls, id_, action)

    @contextmanager
    def transaction(self) -> Iterator["DataAccess"]:
        with db.gateway.transaction() as tx:
            yield DataAccess(tx)


data_access = DataAccess()
