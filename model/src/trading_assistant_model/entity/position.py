from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime
from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class Position(Foundation, table=True):
    """Stores the complete information for every position created by the system. It allows
    the system to identify and track positions that have been opened as well as
    positions that are still pending execution.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="Position",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("user_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("trading_platform_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("broker_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("account_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("trailing_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("partial_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("action_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("action_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("date", FieldType.DATETIME, nullable=False),
            FieldDeclaration("volume", FieldType.DECIMAL, nullable=False),
            FieldDeclaration(
                "profit", FieldType.DECIMAL, nullable=False, default=Decimal(0)
            ),
            FieldDeclaration(
                "is_executed", FieldType.BOOLEAN, nullable=False, default=False
            ),
            FieldDeclaration("order_type", FieldType.STRING, nullable=False),
            FieldDeclaration("base_tp", FieldType.DECIMAL, nullable=False),
            FieldDeclaration("base_sl", FieldType.DECIMAL, nullable=False),
            FieldDeclaration("real_tp", FieldType.DECIMAL, nullable=False),
            FieldDeclaration("real_sl", FieldType.DECIMAL, nullable=False),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(UniqueConstraint(("name",)),),
        references=(
            Reference(("user_id",), "User", ("id",)),
            Reference(("trading_platform_id",), "TradingPlatform", ("id",)),
            Reference(("broker_id",), "Broker", ("id",)),
            Reference(("account_id",), "Account", ("id",)),
            Reference(("trailing_group_id",), "TrailingGroup", ("id",)),
            Reference(("partial_group_id",), "PartialGroup", ("id",)),
            Reference(("action_group_id",), "ActionGroup", ("id",)),
            Reference(("action_id",), "Action", ("id",)),
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the position, assigned automatically.",
    )
    user_id: int = Field(description="Identifies the user who owns the position.")
    name: str = Field(description="The position's display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = Field(
        description="Identifies the broker through which the position is executed."
    )
    account_id: int = Field(
        description="Identifies the trading account used for the position."
    )
    trailing_group_id: int = Field(
        description="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = Field(
        description="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = Field(
        description="Identifies the Action Group associated with the position."
    )
    action_id: int = Field(
        description="Identifies the action from which the position is created."
    )
    date: AwareDatetime = Field(description="Stores the position's date and time.")
    volume: Decimal = Field(description="Stores the position's trading volume.")
    profit: Decimal = Field(
        default=Decimal(0), description="Stores the position's current profit or loss."
    )
    is_executed: bool = Field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = Field(description="Stores the position's order type.")
    base_tp: Decimal = Field(
        description="Stores the position's initial Take Profit value."
    )
    base_sl: Decimal = Field(
        description="Stores the position's initial Stop Loss value."
    )
    real_tp: Decimal = Field(
        description="Stores the position's current Take Profit value."
    )
    real_sl: Decimal = Field(
        description="Stores the position's current Stop Loss value."
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the position is active."
    )
    description: str | None = Field(default=None, description="Describes the position.")
