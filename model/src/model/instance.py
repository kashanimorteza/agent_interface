"""Instance Domain Definition."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class Instance(DomainModel):
    """A user-owned connection instance through which the system accesses a Trading Platform.

    The Target additionally requires that every connection field the selected Trading
    Platform needs be present before the Instance can be used. That requirement depends
    on the referenced Trading Platform's own ``code`` and is therefore not an Intrinsic
    Rule (it cannot be evaluated from Instance's own data alone); it is published here as
    documentation for the consuming Component rather than enforced by Model.
    """

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    user_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("User", "id"))]
    trading_platform_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("TradingPlatform", "id"))
    ]
    name: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    ip: Annotated[str | None, FieldMeta(nullable=True)] = None
    username: Annotated[str | None, FieldMeta(nullable=True)] = None
    password: Annotated[str | None, FieldMeta(nullable=True, credential="encrypted")] = None
    api_key: Annotated[str | None, FieldMeta(nullable=True, credential="encrypted")] = None
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("user_id", "name"),)
