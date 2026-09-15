"""Partial Group Domain Definition."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class PartialGroup(DomainModel):
    """An independent group of rules for closing portions of an open trade."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    user_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("User", "id"))]
    name: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("user_id", "name"),)
