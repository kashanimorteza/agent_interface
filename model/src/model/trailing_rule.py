"""Trailing Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class TrailingRule(DomainModel):
    """An individual rule within a Trailing Group telling the system when and how to trail."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    name: Annotated[str, FieldMeta(nullable=False, unique=True)] = Field(min_length=1)
    trailing_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("TrailingGroup", "id"))
    ]
    trigger_percentage: Annotated[Decimal, FieldMeta(nullable=False)]
    take_profit_adjustment: Annotated[Decimal | None, FieldMeta(nullable=True)] = None
    stop_loss_adjustment: Annotated[Decimal | None, FieldMeta(nullable=True)] = None
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("trailing_group_id", "trigger_percentage"),)
