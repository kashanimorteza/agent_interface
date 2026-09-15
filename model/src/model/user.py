"""The User Domain Definition."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, field_meta


class User(DomainModel):
    """An independent user of the system, enabling multi-user operation."""

    __persistent__ = True

    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    name: str = Field(json_schema_extra=field_meta(unique=True))
    username: str = Field(json_schema_extra=field_meta(unique=True))
    password: str = Field(json_schema_extra=field_meta(credential="hash"))
    api_key: str = Field(json_schema_extra=field_meta(credential="hash"))
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
