"""The Asset Domain Definition."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, field_meta


class Asset(DomainModel):
    """An asset that can be selected for trading, provided by one Broker."""

    __persistent__ = True
    __unique_sets__ = (("broker_id", "symbol"),)

    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    broker_id: int = Field(
        json_schema_extra=field_meta(foreign_key="broker.id", cardinality="many_to_one")
    )
    symbol: str = Field(json_schema_extra=field_meta())
    category: str = Field(json_schema_extra=field_meta())
    point_size: float = Field(default=0.0, json_schema_extra=field_meta())
    digits: int = Field(default=0, json_schema_extra=field_meta())
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
