"""The Instance Domain Definition."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, field_meta


class Instance(DomainModel):
    """A user-owned connection instance through which the system accesses a Trading Platform."""

    __persistent__ = True
    __unique_sets__ = (("user_id", "name"),)

    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    user_id: int = Field(
        json_schema_extra=field_meta(foreign_key="user.id", cardinality="many_to_one")
    )
    trading_platform_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="trading_platform.id", cardinality="many_to_one"
        )
    )
    name: str = Field(json_schema_extra=field_meta())
    ip: str | None = Field(default=None, json_schema_extra=field_meta(nullable=True))
    username: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
    password: str | None = Field(
        default=None,
        json_schema_extra=field_meta(nullable=True, credential="encrypted"),
    )
    api_key: str | None = Field(
        default=None,
        json_schema_extra=field_meta(nullable=True, credential="encrypted"),
    )
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
