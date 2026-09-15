"""Account Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class Account(DomainModel):
    """A funded trading account through which the system executes trades.

    The Target additionally requires that Account credentials are not duplicated with
    Instance credentials unless the selected Trading Platform explicitly requires it in
    both roles. That comparison spans another Domain Definition's stored data and is
    therefore not an Intrinsic Rule; it is published here as documentation for the
    consuming Component rather than enforced by Model.
    """

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    name: Annotated[str, FieldMeta(nullable=False, unique=True)] = Field(min_length=1)
    group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("AccountGroup", "id"))
    ]
    broker_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Broker", "id"))]
    instance_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Instance", "id"))]
    base_currency_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("Currency", "id"))
    ]
    username: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    password: Annotated[str, FieldMeta(nullable=False, credential="encrypted")] = Field(
        min_length=1
    )
    leverage: Annotated[int, FieldMeta(nullable=False)]
    balance: Annotated[Decimal, FieldMeta(nullable=False, default=Decimal("0"))] = Decimal("0")
    account_type: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("group_id", "broker_id", "instance_id"),)
