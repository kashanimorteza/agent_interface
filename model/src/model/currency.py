"""The Currency Domain Definition."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, field_meta


class Currency(DomainModel):
    """A currency usable by the trading system, owned by one User."""

    __persistent__ = True
    __unique_sets__ = (("user_id", "code"),)

    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    user_id: int = Field(
        json_schema_extra=field_meta(foreign_key="user.id", cardinality="many_to_one")
    )
    code: str = Field(json_schema_extra=field_meta())
    symbol: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
    country: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
    decimal_digits: int = Field(default=2, json_schema_extra=field_meta())
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
