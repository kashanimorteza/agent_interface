"""Trading Platform Domain Definition."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, PersistenceMeta


class TradingPlatform(DomainModel):
    """A supported trading API standard, keeping the system independent of any one exchange."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    name: Annotated[str, FieldMeta(nullable=False, unique=True)] = Field(min_length=1)
    code: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
