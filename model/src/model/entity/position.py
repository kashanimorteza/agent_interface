from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Position",
    description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
    fields=(
        identity(),
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
            default=Decimal(0),
        ),
        FieldDeclaration(
            name="is_executed",
            description="Indicates whether the position has been executed.",
            type=FieldType.BOOLEAN,
            nullable=False,
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
        activity("Indicates whether the position is active."),
        FieldDeclaration(
            name="description",
            description="Describes the position.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(
        RelationDeclaration("user_id", "User", "id"),
        RelationDeclaration("trading_platform_id", "Trading Platform", "id"),
        RelationDeclaration("broker_id", "Broker", "id"),
        RelationDeclaration("account_id", "Account", "id"),
        RelationDeclaration("trailing_group_id", "Trailing Group", "id"),
        RelationDeclaration("partial_group_id", "Partial Group", "id"),
        RelationDeclaration("action_group_id", "Action Group", "id"),
        RelationDeclaration("action_id", "Action", "id"),
    ),
    unique_constraints=(UniqueConstraintDeclaration(("name",)),),
)


class Position(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    name: str = column(_DECLARATION, "name")
    trading_platform_id: int = column(_DECLARATION, "trading_platform_id")
    broker_id: int = column(_DECLARATION, "broker_id")
    account_id: int = column(_DECLARATION, "account_id")
    trailing_group_id: int = column(_DECLARATION, "trailing_group_id")
    partial_group_id: int = column(_DECLARATION, "partial_group_id")
    action_group_id: int = column(_DECLARATION, "action_group_id")
    action_id: int = column(_DECLARATION, "action_id")
    date: AwareDatetime = column(_DECLARATION, "date")
    volume: Decimal = column(_DECLARATION, "volume")
    profit: Decimal = column(_DECLARATION, "profit")
    is_executed: bool = column(_DECLARATION, "is_executed")
    order_type: str = column(_DECLARATION, "order_type")
    base_tp: Decimal = column(_DECLARATION, "base_tp")
    base_sl: Decimal = column(_DECLARATION, "base_sl")
    real_tp: Decimal = column(_DECLARATION, "real_tp")
    real_sl: Decimal = column(_DECLARATION, "real_sl")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
