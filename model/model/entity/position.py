"""The Position Entity."""

from decimal import Decimal

from pydantic import AwareDatetime
from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import DecimalText, table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class Position(Entity, table=True):
    """The Position Entity."""

    __tablename__ = "Position"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments()

    declaration = Declaration(
        name="Position",
        description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the position.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The position's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="trading_platform_id",
                description="Identifies the trading platform used to execute the position.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="broker_id",
                description="Identifies the broker through which the position is executed.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="account_id",
                description="Identifies the trading account used for the position.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="trailing_group_id",
                description="Identifies the Trailing Group applied to the position.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="partial_group_id",
                description="Identifies the Partial Group applied to the position.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="action_group_id",
                description="Identifies the Action Group associated with the position.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="action_id",
                description="Identifies the action from which the position is created.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="date",
                description="Stores the position's date and time.",
                type="datetime",
                nullable=False,
            ),
            FieldDeclaration(
                name="volume",
                description="Stores the position's trading volume.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="profit",
                description="Stores the position's current profit or loss.",
                type="decimal",
                nullable=False,
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="is_executed",
                description="Indicates whether the position has been executed.",
                type="boolean",
                nullable=False,
                default=False,
            ),
            FieldDeclaration(
                name="order_type",
                description="Stores the position's order type.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="base_tp",
                description="Stores the position's initial Take Profit value.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="base_sl",
                description="Stores the position's initial Stop Loss value.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="real_tp",
                description="Stores the position's current Take Profit value.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="real_sl",
                description="Stores the position's current Stop Loss value.",
                type="decimal",
                nullable=False,
            ),
            activity_declaration("Indicates whether the position is active."),
            FieldDeclaration(
                name="description",
                description="Describes the position.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="user_id", target_entity="User", target_field="id"
            ),
            RelationDeclaration(
                local_field="trading_platform_id",
                target_entity="Trading Platform",
                target_field="id",
            ),
            RelationDeclaration(
                local_field="broker_id", target_entity="Broker", target_field="id"
            ),
            RelationDeclaration(
                local_field="account_id", target_entity="Account", target_field="id"
            ),
            RelationDeclaration(
                local_field="trailing_group_id",
                target_entity="Trailing Group",
                target_field="id",
            ),
            RelationDeclaration(
                local_field="partial_group_id",
                target_entity="Partial Group",
                target_field="id",
            ),
            RelationDeclaration(
                local_field="action_group_id",
                target_entity="Action Group",
                target_field="id",
            ),
            RelationDeclaration(
                local_field="action_id", target_entity="Action", target_field="id"
            ),
        ),
        unique_constraints=(("name",),),
    )

    id: int | None = identity_field()
    user_id: int = Field(
        foreign_key="User.id", description="Identifies the user who owns the position."
    )
    name: str = Field(unique=True, description="The position's display name.")
    trading_platform_id: int = Field(
        foreign_key="TradingPlatform.id",
        description="Identifies the trading platform used to execute the position.",
    )
    broker_id: int = Field(
        foreign_key="Broker.id",
        description="Identifies the broker through which the position is executed.",
    )
    account_id: int = Field(
        foreign_key="Account.id",
        description="Identifies the trading account used for the position.",
    )
    trailing_group_id: int = Field(
        foreign_key="TrailingGroup.id",
        description="Identifies the Trailing Group applied to the position.",
    )
    partial_group_id: int = Field(
        foreign_key="PartialGroup.id",
        description="Identifies the Partial Group applied to the position.",
    )
    action_group_id: int = Field(
        foreign_key="ActionGroup.id",
        description="Identifies the Action Group associated with the position.",
    )
    action_id: int = Field(
        foreign_key="Action.id",
        description="Identifies the action from which the position is created.",
    )
    date: AwareDatetime = Field(description="Stores the position's date and time.")
    volume: Decimal = Field(
        sa_type=DecimalText, description="Stores the position's trading volume."
    )
    profit: Decimal = Field(
        default=Decimal(0),
        sa_type=DecimalText,
        description="Stores the position's current profit or loss.",
    )
    is_executed: bool = Field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = Field(description="Stores the position's order type.")
    base_tp: Decimal = Field(
        sa_type=DecimalText,
        description="Stores the position's initial Take Profit value.",
    )
    base_sl: Decimal = Field(
        sa_type=DecimalText,
        description="Stores the position's initial Stop Loss value.",
    )
    real_tp: Decimal = Field(
        sa_type=DecimalText,
        description="Stores the position's current Take Profit value.",
    )
    real_sl: Decimal = Field(
        sa_type=DecimalText,
        description="Stores the position's current Stop Loss value.",
    )
    is_active: bool = activity_field("Indicates whether the position is active.")
    description: str | None = Field(default=None, description="Describes the position.")
