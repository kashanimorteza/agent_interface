"""The Position Entity."""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class Position(Entity, table=True):
    """The Position Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Position",
        description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the user who owns the position.",
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The position's display name.",
            ),
            FieldDeclaration(
                name="trading_platform_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the trading platform used to execute the position.",
            ),
            FieldDeclaration(
                name="broker_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the broker through which the position is executed.",
            ),
            FieldDeclaration(
                name="account_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the trading account used for the position.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the Trailing Group applied to the position.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the Partial Group applied to the position.",
            ),
            FieldDeclaration(
                name="action_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the Action Group associated with the position.",
            ),
            FieldDeclaration(
                name="action_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the action from which the position is created.",
            ),
            FieldDeclaration(
                name="date",
                type=FieldType.DATETIME,
                nullable=False,
                description="Stores the position's date and time.",
            ),
            FieldDeclaration(
                name="volume",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Stores the position's trading volume.",
            ),
            FieldDeclaration(
                name="profit",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Stores the position's current profit or loss.",
                has_default=True,
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="is_executed",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the position has been executed.",
                has_default=True,
                default=False,
            ),
            FieldDeclaration(
                name="order_type",
                type=FieldType.STRING,
                nullable=False,
                description="Stores the position's order type.",
            ),
            FieldDeclaration(
                name="base_tp",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Stores the position's initial Take Profit value.",
            ),
            FieldDeclaration(
                name="base_sl",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Stores the position's initial Stop Loss value.",
            ),
            FieldDeclaration(
                name="real_tp",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Stores the position's current Take Profit value.",
            ),
            FieldDeclaration(
                name="real_sl",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Stores the position's current Stop Loss value.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the position is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the position.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
            Relation(
                local_field="trading_platform_id",
                target_entity="Trading Platform",
                target_field="id",
            ),
            Relation(
                local_field="broker_id", target_entity="Broker", target_field="id"
            ),
            Relation(
                local_field="account_id", target_entity="Account", target_field="id"
            ),
            Relation(
                local_field="trailing_group_id",
                target_entity="Trailing Group",
                target_field="id",
            ),
            Relation(
                local_field="partial_group_id",
                target_entity="Partial Group",
                target_field="id",
            ),
            Relation(
                local_field="action_group_id",
                target_entity="Action Group",
                target_field="id",
            ),
            Relation(
                local_field="action_id", target_entity="Action", target_field="id"
            ),
        ),
        unique_constraints=(UniqueConstraint(fields=("name",)),),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    name: str = Field(unique=True)
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
