"""The Trading Platform Domain Definition."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, field_meta


class TradingPlatform(DomainModel):
    """A supported trading API standard, such as MetaTrader 5 or Binance."""

    __persistent__ = True

    id: int | None = Field(
        default=None,
        json_schema_extra=field_meta(
            nullable=False, primary_key=True, auto_increment=True
        ),
    )
    name: str = Field(json_schema_extra=field_meta(unique=True))
    code: str = Field(json_schema_extra=field_meta())
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
