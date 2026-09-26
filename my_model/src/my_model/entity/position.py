"""Position Domain Entity."""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    ReferenceDeclaration,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Position(ModelFoundation, table=True):
    """Stores the complete information for every position created by the system."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Position",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", LogicalType.INTEGER),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("trading_platform_id", LogicalType.INTEGER),
            FieldDeclaration("broker_id", LogicalType.INTEGER),
            FieldDeclaration("account_id", LogicalType.INTEGER),
            FieldDeclaration("trailing_group_id", LogicalType.INTEGER),
            FieldDeclaration("partial_group_id", LogicalType.INTEGER),
            FieldDeclaration("action_group_id", LogicalType.INTEGER),
            FieldDeclaration("action_id", LogicalType.INTEGER),
            FieldDeclaration("date", LogicalType.DATETIME),
            FieldDeclaration("volume", LogicalType.DECIMAL),
            FieldDeclaration("profit", LogicalType.DECIMAL, default=Decimal(0)),
            FieldDeclaration("is_executed", LogicalType.BOOLEAN, default=False),
            FieldDeclaration("order_type", LogicalType.STRING),
            FieldDeclaration("base_tp", LogicalType.DECIMAL),
            FieldDeclaration("base_sl", LogicalType.DECIMAL),
            FieldDeclaration("real_tp", LogicalType.DECIMAL),
            FieldDeclaration("real_sl", LogicalType.DECIMAL),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(
            ReferenceDeclaration("user_id", "User"),
            ReferenceDeclaration("trading_platform_id", "Trading Platform"),
            ReferenceDeclaration("broker_id", "Broker"),
            ReferenceDeclaration("account_id", "Account"),
            ReferenceDeclaration("trailing_group_id", "Trailing Group"),
            ReferenceDeclaration("partial_group_id", "Partial Group"),
            ReferenceDeclaration("action_group_id", "Action Group"),
            ReferenceDeclaration("action_id", "Action"),
        ),
        unique_constraints=(("name",),),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(unique=True)
    trading_platform_id: int = Field(foreign_key="tradingplatform.id")
    broker_id: int = Field(foreign_key="broker.id")
    account_id: int = Field(foreign_key="account.id")
    trailing_group_id: int = Field(foreign_key="trailinggroup.id")
    partial_group_id: int = Field(foreign_key="partialgroup.id")
    action_group_id: int = Field(foreign_key="actiongroup.id")
    action_id: int = Field(foreign_key="action.id")
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
