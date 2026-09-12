"""Database Interface: Logic's only route to the public Database interface.

Translates Logic's data operations into calls on the generic Database
interface and connects a Logic-requested group of operations to Database's
public transaction boundary on one resolved Instance. Contains no
application Behaviour and decides nothing about which operations belong
together — that decision belongs to Logic.
"""

from __future__ import annotations

from typing import Any, Literal

from my_database import interface as _db_interface
from my_database.interface import (
    ConstraintViolationError,
    NotFoundError,
    Transaction,
    UnsupportedOperationError,
)
from my_model._base import BaseModel

__all__ = [
    "ConstraintViolationError",
    "NotFoundError",
    "Transaction",
    "UnsupportedOperationError",
    "create",
    "delete",
    "get",
    "list_",
    "set_status",
    "transaction",
    "update",
]


def transaction(instance: str | None = None):
    return _db_interface.transaction(instance)


def create[T: BaseModel](
    record: T, *, instance: str | None = None, within: Transaction | None = None
) -> T:
    return _db_interface.add(record, instance=instance, within=within)


def get[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    *,
    instance: str | None = None,
    within: Transaction | None = None,
) -> T | None:
    return _db_interface.get(model_cls, record_id, instance=instance, within=within)


def list_[T: BaseModel](
    model_cls: type[T],
    *,
    instance: str | None = None,
    within: Transaction | None = None,
    order_by: str | None = "id",
    limit: int | None = None,
    offset: int | None = None,
    **filters: Any,
) -> list[T]:
    return _db_interface.list_(
        model_cls,
        instance=instance,
        within=within,
        order_by=order_by,
        limit=limit,
        offset=offset,
        **filters,
    )


def update[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    *,
    instance: str | None = None,
    within: Transaction | None = None,
    **changes: Any,
) -> T:
    return _db_interface.update(
        model_cls, record_id, instance=instance, within=within, **changes
    )


def delete[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    *,
    instance: str | None = None,
    within: Transaction | None = None,
) -> bool:
    return _db_interface.delete(model_cls, record_id, instance=instance, within=within)


def set_status[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    action: Literal["enable", "disable"],
    *,
    instance: str | None = None,
    within: Transaction | None = None,
) -> T:
    return _db_interface.set_status(
        model_cls, record_id, action, instance=instance, within=within
    )
