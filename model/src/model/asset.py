"""Asset Domain Definition."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class Asset(DomainModel):
    """An asset selectable for trading, identifying its broker and category."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    broker_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Broker", "id"))]
    symbol: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    category: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    point_size: Annotated[float, FieldMeta(nullable=False, default=0.0)] = 0.0
    digits: Annotated[int, FieldMeta(nullable=False, default=0)] = 0
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("broker_id", "symbol"),)
