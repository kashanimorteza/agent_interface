"""Partial Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class PartialRule(DomainModel):
    """An individual Partial Close rule telling the system when and how much to close."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    name: Annotated[str, FieldMeta(nullable=False, unique=True)] = Field(min_length=1)
    partial_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("PartialGroup", "id"))
    ]
    profit_percentage: Annotated[Decimal, FieldMeta(nullable=False)]
    close_percentage: Annotated[Decimal, FieldMeta(nullable=False)]
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("partial_group_id", "profit_percentage"),)
