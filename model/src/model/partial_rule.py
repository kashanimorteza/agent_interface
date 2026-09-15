"""The Partial Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel, field_meta


class PartialRule(DomainModel):
    """One partial-close condition within a Partial Group."""

    __persistent__ = True
    __unique_sets__ = (("partial_group_id", "profit_percentage"),)

    id: int | None = Field(
        default=None,
        json_schema_extra=field_meta(
            nullable=False, primary_key=True, auto_increment=True
        ),
    )
    name: str = Field(json_schema_extra=field_meta(unique=True))
    partial_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="partial_group.id", cardinality="many_to_one"
        )
    )
    profit_percentage: Decimal = Field(json_schema_extra=field_meta())
    close_percentage: Decimal = Field(json_schema_extra=field_meta())
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
