"""Broker Domain Definition."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class Broker(DomainModel):
    """A broker supported by the system, decoupled from any one Trading Platform."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    name: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    user_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("User", "id"))]
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("user_id", "name"),)
