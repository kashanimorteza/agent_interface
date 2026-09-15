"""Position Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import AwareDatetime, Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class Position(DomainModel):
    """The complete information for every position created by the system, pending or opened."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    user_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("User", "id"))]
    name: Annotated[str, FieldMeta(nullable=False, unique=True)] = Field(min_length=1)
    trading_platform_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("TradingPlatform", "id"))
    ]
    broker_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Broker", "id"))]
    account_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Account", "id"))]
    trailing_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("TrailingGroup", "id"))
    ]
    partial_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("PartialGroup", "id"))
    ]
    action_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("ActionGroup", "id"))
    ]
    action_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Action", "id"))]
    date: Annotated[AwareDatetime, FieldMeta(nullable=False)]
    volume: Annotated[Decimal, FieldMeta(nullable=False)]
    profit: Annotated[Decimal, FieldMeta(nullable=False, default=Decimal("0"))] = Decimal("0")
    is_executed: Annotated[bool, FieldMeta(nullable=False, default=False)] = False
    order_type: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    base_tp: Annotated[Decimal, FieldMeta(nullable=False)]
    base_sl: Annotated[Decimal, FieldMeta(nullable=False)]
    real_tp: Annotated[Decimal, FieldMeta(nullable=False)]
    real_sl: Annotated[Decimal, FieldMeta(nullable=False)]
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
