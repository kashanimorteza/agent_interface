"""Currency Domain Definition."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class Currency(DomainModel):
    """A currency usable by the trading system, with its code, symbol, region, and precision."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    user_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("User", "id"))]
    code: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=3, max_length=3)
    symbol: Annotated[str | None, FieldMeta(nullable=True)] = None
    country: Annotated[str | None, FieldMeta(nullable=True)] = None
    decimal_digits: Annotated[int, FieldMeta(nullable=False, default=2)] = 2
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("user_id", "code"),)
