"""Position Entity."""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Position(ModelFoundation, table=True):
    """Stores the complete information for every position created by the system."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Position",
        purpose="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "user_id",
                LogicalType.INTEGER,
                purpose="Identifies the user who owns the position",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The position's display name"
            ),
            FieldDeclaration(
                "trading_platform_id",
                LogicalType.INTEGER,
                purpose="Identifies the trading platform used to execute the position",
            ),
            FieldDeclaration(
                "broker_id",
                LogicalType.INTEGER,
                purpose="Identifies the broker through which the position is executed",
            ),
            FieldDeclaration(
                "account_id",
                LogicalType.INTEGER,
                purpose="Identifies the trading account used for the position",
            ),
            FieldDeclaration(
                "trailing_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the Trailing Group applied to the position",
            ),
            FieldDeclaration(
                "partial_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the Partial Group applied to the position",
            ),
            FieldDeclaration(
                "action_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the Action Group associated with the position",
            ),
            FieldDeclaration(
                "action_id",
                LogicalType.INTEGER,
                purpose="Identifies the action from which the position is created",
            ),
            FieldDeclaration(
                "date",
                LogicalType.DATETIME,
                purpose="Stores the position's date and time",
            ),
            FieldDeclaration(
                "volume",
                LogicalType.DECIMAL,
                purpose="Stores the position's trading volume",
            ),
            FieldDeclaration(
                "profit",
                LogicalType.DECIMAL,
                has_default=True,
                default=Decimal(0),
                purpose="Stores the position's current profit or loss",
            ),
            FieldDeclaration(
                "is_executed",
                LogicalType.BOOLEAN,
                has_default=True,
                default=False,
                purpose="Indicates whether the position has been executed",
            ),
            FieldDeclaration(
                "order_type",
                LogicalType.STRING,
                purpose="Stores the position's order type",
            ),
            FieldDeclaration(
                "base_tp",
                LogicalType.DECIMAL,
                purpose="Stores the position's initial Take Profit value",
            ),
            FieldDeclaration(
                "base_sl",
                LogicalType.DECIMAL,
                purpose="Stores the position's initial Stop Loss value",
            ),
            FieldDeclaration(
                "real_tp",
                LogicalType.DECIMAL,
                purpose="Stores the position's current Take Profit value",
            ),
            FieldDeclaration(
                "real_sl",
                LogicalType.DECIMAL,
                purpose="Stores the position's current Stop Loss value",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the position is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the position",
            ),
        ),
        references=(
            Reference("user_id", "User", "id", RelationshipKind.BELONGS_TO),
            Reference(
                "trading_platform_id", "TradingPlatform", "id", RelationshipKind.USES
            ),
            Reference("broker_id", "Broker", "id", RelationshipKind.USES),
            Reference("account_id", "Account", "id", RelationshipKind.USES),
            Reference(
                "trailing_group_id", "TrailingGroup", "id", RelationshipKind.USES
            ),
            Reference("partial_group_id", "PartialGroup", "id", RelationshipKind.USES),
            Reference("action_group_id", "ActionGroup", "id", RelationshipKind.USES),
            Reference("action_id", "Action", "id", RelationshipKind.BELONGS_TO),
        ),
        unique_constraints=(UniquenessConstraint(("name",)),),
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
