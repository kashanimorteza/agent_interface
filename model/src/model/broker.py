"""The Broker Domain Definition."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, field_meta


class Broker(DomainModel):
    """A broker supported by the system, owned by one User."""

    __persistent__ = True
    __unique_sets__ = (("user_id", "name"),)

    id: int | None = Field(
        default=None,
        json_schema_extra=field_meta(
            nullable=False, primary_key=True, auto_increment=True
        ),
    )
    name: str = Field(json_schema_extra=field_meta())
    user_id: int = Field(
        json_schema_extra=field_meta(foreign_key="user.id", cardinality="many_to_one")
    )
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
