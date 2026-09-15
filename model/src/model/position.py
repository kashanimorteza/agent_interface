"""The Position Domain Definition."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_validator

from model.foundation import DomainModel, field_meta


class Position(DomainModel):
    """The complete information for one position created by the system."""

    __persistent__ = True

    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    user_id: int = Field(
        json_schema_extra=field_meta(foreign_key="user.id", cardinality="many_to_one")
    )
    name: str = Field(json_schema_extra=field_meta(unique=True))
    trading_platform_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="trading_platform.id", cardinality="many_to_one"
        )
    )
    broker_id: int = Field(
        json_schema_extra=field_meta(foreign_key="broker.id", cardinality="many_to_one")
    )
    account_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="account.id", cardinality="many_to_one"
        )
    )
    trailing_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="trailing_group.id", cardinality="many_to_one"
        )
    )
    partial_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="partial_group.id", cardinality="many_to_one"
        )
    )
    action_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="action_group.id", cardinality="many_to_one"
        )
    )
    action_id: int = Field(
        json_schema_extra=field_meta(foreign_key="action.id", cardinality="many_to_one")
    )
    date: datetime = Field(json_schema_extra=field_meta())
    volume: Decimal = Field(json_schema_extra=field_meta())
    profit: Decimal = Field(default=Decimal(0), json_schema_extra=field_meta())
    is_executed: bool = Field(default=False, json_schema_extra=field_meta())
    order_type: str = Field(json_schema_extra=field_meta())
    base_tp: Decimal = Field(json_schema_extra=field_meta())
    base_sl: Decimal = Field(json_schema_extra=field_meta())
    real_tp: Decimal = Field(json_schema_extra=field_meta())
    real_sl: Decimal = Field(json_schema_extra=field_meta())
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )

    @field_validator("date")
    @classmethod
    def _date_is_timezone_aware(cls, value: datetime) -> datetime:
        """Preserve the timezone-aware absolute-instant convention for this Field."""
        if value.tzinfo is None:
            raise ValueError("date must be timezone-aware")
        return value
