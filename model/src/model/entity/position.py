"""Entity: Position."""

from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    Unique,
    ValueGeneration,
)
from model.foundation import Foundation


class Position(Foundation, table=True):
    """Position Entity."""

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
    date: AwareDatetime
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

    declaration: ClassVar[Declaration] = Declaration(
        entity="Position",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, value_generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", FieldType.INTEGER),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("trading_platform_id", FieldType.INTEGER),
            FieldDeclaration("broker_id", FieldType.INTEGER),
            FieldDeclaration("account_id", FieldType.INTEGER),
            FieldDeclaration("trailing_group_id", FieldType.INTEGER),
            FieldDeclaration("partial_group_id", FieldType.INTEGER),
            FieldDeclaration("action_group_id", FieldType.INTEGER),
            FieldDeclaration("action_id", FieldType.INTEGER),
            FieldDeclaration("date", FieldType.DATETIME),
            FieldDeclaration("volume", FieldType.DECIMAL),
            FieldDeclaration("profit", FieldType.DECIMAL, default=Decimal(0)),
            FieldDeclaration("is_executed", FieldType.BOOLEAN, default=False),
            FieldDeclaration("order_type", FieldType.STRING),
            FieldDeclaration("base_tp", FieldType.DECIMAL),
            FieldDeclaration("base_sl", FieldType.DECIMAL),
            FieldDeclaration("real_tp", FieldType.DECIMAL),
            FieldDeclaration("real_sl", FieldType.DECIMAL),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(
            Reference("user_id", "User"),
            Reference("trading_platform_id", "TradingPlatform"),
            Reference("broker_id", "Broker"),
            Reference("account_id", "Account"),
            Reference("trailing_group_id", "TrailingGroup"),
            Reference("partial_group_id", "PartialGroup"),
            Reference("action_group_id", "ActionGroup"),
            Reference("action_id", "Action"),
        ),
        uniques=(Unique(("name",)),),
    )
