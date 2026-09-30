"""The Position Entity."""

from decimal import Decimal
from typing import ClassVar

from ..core.base import EntityBase, UtcDatetime
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)


class Position(EntityBase):
    """The Position Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Position",
        description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the position.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The position's display name.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="trading_platform_id",
                description="Identifies the trading platform used to execute the position.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="broker_id",
                description="Identifies the broker through which the position is executed.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="account_id",
                description="Identifies the trading account used for the position.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="trailing_group_id",
                description="Identifies the Trailing Group applied to the position.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="partial_group_id",
                description="Identifies the Partial Group applied to the position.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="action_group_id",
                description="Identifies the Action Group associated with the position.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="action_id",
                description="Identifies the action from which the position is created.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="date",
                description="Stores the position's date and time.",
                type=FieldType.DATETIME,
                nullable=False,
            ),
            FieldDeclaration(
                name="volume",
                description="Stores the position's trading volume.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="profit",
                description="Stores the position's current profit or loss.",
                type=FieldType.DECIMAL,
                nullable=False,
                has_default=True,
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="is_executed",
                description="Indicates whether the position has been executed.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=False,
            ),
            FieldDeclaration(
                name="order_type",
                description="Stores the position's order type.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="base_tp",
                description="Stores the position's initial Take Profit value.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="base_sl",
                description="Stores the position's initial Stop Loss value.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="real_tp",
                description="Stores the position's current Take Profit value.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="real_sl",
                description="Stores the position's current Stop Loss value.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the position is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the position.",
                type=FieldType.STRING,
                nullable=True,
            ),
        ),
        primary_key="id",
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
    date: UtcDatetime
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
