from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class Position(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Position",
        description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
        fields=(
            FieldDeclaration(
                name="id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the user who owns the position.",
            ),
            FieldDeclaration(
                name="name",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The position's display name.",
            ),
            FieldDeclaration(
                name="trading_platform_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the trading platform used to execute the position.",
            ),
            FieldDeclaration(
                name="broker_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the broker through which the position is executed.",
            ),
            FieldDeclaration(
                name="account_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the trading account used for the position.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the Trailing Group applied to the position.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the Partial Group applied to the position.",
            ),
            FieldDeclaration(
                name="action_group_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the Action Group associated with the position.",
            ),
            FieldDeclaration(
                name="action_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the action from which the position is created.",
            ),
            FieldDeclaration(
                name="date",
                type=LogicalType.DATETIME,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Stores the position's date and time.",
            ),
            FieldDeclaration(
                name="volume",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Stores the position's trading volume.",
            ),
            FieldDeclaration(
                name="profit",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=True,
                default=Decimal(0),
                immutable=False,
                description="Stores the position's current profit or loss.",
            ),
            FieldDeclaration(
                name="is_executed",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=False,
                immutable=False,
                description="Indicates whether the position has been executed.",
            ),
            FieldDeclaration(
                name="order_type",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Stores the position's order type.",
            ),
            FieldDeclaration(
                name="base_tp",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Stores the position's initial Take Profit value.",
            ),
            FieldDeclaration(
                name="base_sl",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Stores the position's initial Stop Loss value.",
            ),
            FieldDeclaration(
                name="real_tp",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Stores the position's current Take Profit value.",
            ),
            FieldDeclaration(
                name="real_sl",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Stores the position's current Stop Loss value.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the position is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
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
            Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
            Relation(local_field="account_id", target_entity="Account", target_field="id"),
            Relation(
                local_field="trailing_group_id", target_entity="Trailing Group", target_field="id"
            ),
            Relation(
                local_field="partial_group_id", target_entity="Partial Group", target_field="id"
            ),
            Relation(
                local_field="action_group_id", target_entity="Action Group", target_field="id"
            ),
            Relation(local_field="action_id", target_entity="Action", target_field="id"),
        ),
        unique_constraints=(("name",),),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
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
