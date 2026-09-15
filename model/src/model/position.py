"""The Position Domain Definition."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import field_validator

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class Position(DomainModel):
    """Stores the complete information for every position created by the
    system.

    Allows the system to identify and track positions that have been opened
    as well as positions that are still pending execution.
    """

    id: int | None = None
    user_id: int
    name: str
    trading_platform_id: int
    broker_id: int
    account_id: int
    trailing_group_id: int
    partial_group_id: int
    action_group_id: int
    action_id: int
    date: datetime
    volume: Decimal
    profit: Decimal = Decimal(0)
    is_executed: bool = False
    order_type: str
    base_tp: Decimal
    base_sl: Decimal
    real_tp: Decimal
    real_sl: Decimal
    is_active: bool = True
    description: str | None = None

    @field_validator("date")
    @classmethod
    def _require_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("date must be timezone-aware")
        return value

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "user_id": FieldContract(nullable=False),
            "name": FieldContract(unique=True, nullable=False),
            "trading_platform_id": FieldContract(nullable=False),
            "broker_id": FieldContract(nullable=False),
            "account_id": FieldContract(nullable=False),
            "trailing_group_id": FieldContract(nullable=False),
            "partial_group_id": FieldContract(nullable=False),
            "action_group_id": FieldContract(nullable=False),
            "action_id": FieldContract(nullable=False),
            "date": FieldContract(nullable=False),
            "volume": FieldContract(nullable=False),
            "profit": FieldContract(nullable=False, default=Decimal(0)),
            "is_executed": FieldContract(nullable=False, default=False),
            "order_type": FieldContract(nullable=False),
            "base_tp": FieldContract(nullable=False),
            "base_sl": FieldContract(nullable=False),
            "real_tp": FieldContract(nullable=False),
            "real_sl": FieldContract(nullable=False),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(
            RelationshipContract(field="user_id", references="User"),
            RelationshipContract(
                field="trading_platform_id", references="TradingPlatform"
            ),
            RelationshipContract(field="broker_id", references="Broker"),
            RelationshipContract(field="account_id", references="Account"),
            RelationshipContract(field="trailing_group_id", references="TrailingGroup"),
            RelationshipContract(field="partial_group_id", references="PartialGroup"),
            RelationshipContract(field="action_group_id", references="ActionGroup"),
            RelationshipContract(field="action_id", references="Action"),
        ),
    )
