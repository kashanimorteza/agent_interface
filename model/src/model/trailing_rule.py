"""The Trailing Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel, field_meta


class TrailingRule(DomainModel):
    """One activation condition and adjustment within a Trailing Group."""

    __persistent__ = True
    __unique_sets__ = (("trailing_group_id", "trigger_percentage"),)

    id: int | None = Field(
        default=None,
        json_schema_extra=field_meta(
            nullable=False, primary_key=True, auto_increment=True
        ),
    )
    name: str = Field(json_schema_extra=field_meta(unique=True))
    trailing_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="trailing_group.id", cardinality="many_to_one"
        )
    )
    trigger_percentage: Decimal = Field(json_schema_extra=field_meta())
    take_profit_adjustment: Decimal | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
