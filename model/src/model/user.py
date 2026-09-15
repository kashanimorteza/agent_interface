"""User Domain Definition."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, PersistenceMeta


class User(DomainModel):
    """An independent user of the system, enabling multi-user operation."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    name: Annotated[str, FieldMeta(nullable=False, unique=True)] = Field(min_length=1)
    username: Annotated[str, FieldMeta(nullable=False, unique=True)] = Field(min_length=1)
    password: Annotated[str, FieldMeta(nullable=False, credential="hash")] = Field(min_length=1)
    api_key: Annotated[str, FieldMeta(nullable=False, credential="hash")] = Field(min_length=1)
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
