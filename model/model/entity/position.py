from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime
from sqlalchemy import Identity
from sqlmodel import Field

from model.core._base import EntityBase
from model.core._columns import DecimalText, UtcDateTime
from model.core.declaration import Declaration, FieldDeclaration, Relation


class Position(EntityBase, table=True):
    __table_args__ = ({"sqlite_autoincrement": True},)
    declaration: ClassVar[Declaration] = Declaration(
        "Position",
        "Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("user_id", "Identifies the user who owns the position.", "integer", False),
            FieldDeclaration("name", "The position's display name.", "string", False),
            FieldDeclaration(
                "trading_platform_id", "Identifies the trading platform used to execute the position.", "integer", False
            ),
            FieldDeclaration(
                "broker_id", "Identifies the broker through which the position is executed.", "integer", False
            ),
            FieldDeclaration("account_id", "Identifies the trading account used for the position.", "integer", False),
            FieldDeclaration(
                "trailing_group_id", "Identifies the Trailing Group applied to the position.", "integer", False
            ),
            FieldDeclaration(
                "partial_group_id", "Identifies the Partial Group applied to the position.", "integer", False
            ),
            FieldDeclaration(
                "action_group_id", "Identifies the Action Group associated with the position.", "integer", False
            ),
            FieldDeclaration(
                "action_id", "Identifies the action from which the position is created.", "integer", False
            ),
            FieldDeclaration("date", "Stores the position's date and time.", "datetime", False),
            FieldDeclaration("volume", "Stores the position's trading volume.", "decimal", False),
            FieldDeclaration(
                "profit",
                "Stores the position's current profit or loss.",
                "decimal",
                False,
                has_default=True,
                default=Decimal("0"),
            ),
            FieldDeclaration(
                "is_executed",
                "Indicates whether the position has been executed.",
                "boolean",
                False,
                has_default=True,
                default=False,
            ),
            FieldDeclaration("order_type", "Stores the position's order type.", "string", False),
            FieldDeclaration("base_tp", "Stores the position's initial Take Profit value.", "decimal", False),
            FieldDeclaration("base_sl", "Stores the position's initial Stop Loss value.", "decimal", False),
            FieldDeclaration("real_tp", "Stores the position's current Take Profit value.", "decimal", False),
            FieldDeclaration("real_sl", "Stores the position's current Stop Loss value.", "decimal", False),
            FieldDeclaration(
                "is_active",
                "Indicates whether the position is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the position.", "string", True),
        ),
        "id",
        relations=(
            Relation("user_id", "User", "id"),
            Relation("trading_platform_id", "Trading Platform", "id"),
            Relation("broker_id", "Broker", "id"),
            Relation("account_id", "Account", "id"),
            Relation("trailing_group_id", "Trailing Group", "id"),
            Relation("partial_group_id", "Partial Group", "id"),
            Relation("action_group_id", "Action Group", "id"),
            Relation("action_id", "Action", "id"),
        ),
        unique_constraints=(("name",),),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    user_id: int = Field(foreign_key="User.id", description="Identifies the user who owns the position.")
    name: str = Field(unique=True, description="The position's display name.")
    trading_platform_id: int = Field(
        foreign_key="TradingPlatform.id", description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = Field(
        foreign_key="Broker.id", description="Identifies the broker through which the position is executed."
    )
    account_id: int = Field(
        foreign_key="Account.id", description="Identifies the trading account used for the position."
    )
    trailing_group_id: int = Field(
        foreign_key="TrailingGroup.id", description="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = Field(
        foreign_key="PartialGroup.id", description="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = Field(
        foreign_key="ActionGroup.id", description="Identifies the Action Group associated with the position."
    )
    action_id: int = Field(
        foreign_key="Action.id", description="Identifies the action from which the position is created."
    )
    date: AwareDatetime = Field(sa_type=UtcDateTime, description="Stores the position's date and time.")
    volume: Decimal = Field(sa_type=DecimalText, description="Stores the position's trading volume.")
    profit: Decimal = Field(
        default=Decimal("0"), sa_type=DecimalText, description="Stores the position's current profit or loss."
    )
    is_executed: bool = Field(default=False, description="Indicates whether the position has been executed.")
    order_type: str = Field(description="Stores the position's order type.")
    base_tp: Decimal = Field(sa_type=DecimalText, description="Stores the position's initial Take Profit value.")
    base_sl: Decimal = Field(sa_type=DecimalText, description="Stores the position's initial Stop Loss value.")
    real_tp: Decimal = Field(sa_type=DecimalText, description="Stores the position's current Take Profit value.")
    real_sl: Decimal = Field(sa_type=DecimalText, description="Stores the position's current Stop Loss value.")
    is_active: bool = Field(default=True, description="Indicates whether the position is active.")
    description: str | None = Field(default=None, description="Describes the position.")
