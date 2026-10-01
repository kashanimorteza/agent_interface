"""The Position Entity."""

from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime
from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Position",
    description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
            type="integer",
            nullable=False,
            immutable=True,
            value_generation="auto_increment",
        ),
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
            has_default=True,
            default=Decimal(0),
        ),
        FieldDeclaration(
            name="is_executed",
            description="Indicates whether the position has been executed.",
            type="boolean",
            nullable=False,
            has_default=True,
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
        FieldDeclaration(
            name="is_active",
            description="Indicates whether the position is active.",
            type="boolean",
            nullable=False,
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            description="Describes the position.",
            type="string",
            nullable=True,
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
        Relation(local_field="action_id", target_entity="Action", target_field="id"),
    ),
    unique_constraints=(("name",),),
    indexes=(),
)


class Position(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    user_id: int = Field(
        description="Identifies the user who owns the position.",
        **column_options(_DECLARATION, "user_id"),
    )
    name: str = Field(
        description="The position's display name.",
        **column_options(_DECLARATION, "name"),
    )
    trading_platform_id: int = Field(
        description="Identifies the trading platform used to execute the position.",
        **column_options(_DECLARATION, "trading_platform_id"),
    )
    broker_id: int = Field(
        description="Identifies the broker through which the position is executed.",
        **column_options(_DECLARATION, "broker_id"),
    )
    account_id: int = Field(
        description="Identifies the trading account used for the position.",
        **column_options(_DECLARATION, "account_id"),
    )
    trailing_group_id: int = Field(
        description="Identifies the Trailing Group applied to the position.",
        **column_options(_DECLARATION, "trailing_group_id"),
    )
    partial_group_id: int = Field(
        description="Identifies the Partial Group applied to the position.",
        **column_options(_DECLARATION, "partial_group_id"),
    )
    action_group_id: int = Field(
        description="Identifies the Action Group associated with the position.",
        **column_options(_DECLARATION, "action_group_id"),
    )
    action_id: int = Field(
        description="Identifies the action from which the position is created.",
        **column_options(_DECLARATION, "action_id"),
    )
    date: AwareDatetime = Field(
        description="Stores the position's date and time.",
        **column_options(_DECLARATION, "date"),
    )
    volume: Decimal = Field(
        description="Stores the position's trading volume.",
        **column_options(_DECLARATION, "volume"),
    )
    profit: Decimal = Field(
        default=Decimal(0),
        description="Stores the position's current profit or loss.",
        **column_options(_DECLARATION, "profit"),
    )
    is_executed: bool = Field(
        default=False,
        description="Indicates whether the position has been executed.",
        **column_options(_DECLARATION, "is_executed"),
    )
    order_type: str = Field(
        description="Stores the position's order type.",
        **column_options(_DECLARATION, "order_type"),
    )
    base_tp: Decimal = Field(
        description="Stores the position's initial Take Profit value.",
        **column_options(_DECLARATION, "base_tp"),
    )
    base_sl: Decimal = Field(
        description="Stores the position's initial Stop Loss value.",
        **column_options(_DECLARATION, "base_sl"),
    )
    real_tp: Decimal = Field(
        description="Stores the position's current Take Profit value.",
        **column_options(_DECLARATION, "real_tp"),
    )
    real_sl: Decimal = Field(
        description="Stores the position's current Stop Loss value.",
        **column_options(_DECLARATION, "real_sl"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the position is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the position.",
        **column_options(_DECLARATION, "description"),
    )
