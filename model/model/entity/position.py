"""The Position Entity."""

from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Position",
    description=(
        "Stores the complete information for every position created by the "
        "system. It allows the system to identify and track positions that "
        "have been opened as well as positions that are still pending "
        "execution."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the user who owns the position.",
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The position's display name.",
        ),
        FieldDeclaration(
            name="trading_platform_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the trading platform used to execute the position.",
        ),
        FieldDeclaration(
            name="broker_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the broker through which the position is executed.",
        ),
        FieldDeclaration(
            name="account_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the trading account used for the position.",
        ),
        FieldDeclaration(
            name="trailing_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the Trailing Group applied to the position.",
        ),
        FieldDeclaration(
            name="partial_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the Partial Group applied to the position.",
        ),
        FieldDeclaration(
            name="action_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the Action Group associated with the position.",
        ),
        FieldDeclaration(
            name="action_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the action from which the position is created.",
        ),
        FieldDeclaration(
            name="date",
            type=FieldType.datetime,
            nullable=False,
            description="Stores the position's date and time.",
        ),
        FieldDeclaration(
            name="volume",
            type=FieldType.decimal,
            nullable=False,
            description="Stores the position's trading volume.",
        ),
        FieldDeclaration(
            name="profit",
            type=FieldType.decimal,
            nullable=False,
            description="Stores the position's current profit or loss.",
            has_default=True,
            default=Decimal("0"),
        ),
        FieldDeclaration(
            name="is_executed",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the position has been executed.",
            has_default=True,
            default=False,
        ),
        FieldDeclaration(
            name="order_type",
            type=FieldType.string,
            nullable=False,
            description="Stores the position's order type.",
        ),
        FieldDeclaration(
            name="base_tp",
            type=FieldType.decimal,
            nullable=False,
            description="Stores the position's initial Take Profit value.",
        ),
        FieldDeclaration(
            name="base_sl",
            type=FieldType.decimal,
            nullable=False,
            description="Stores the position's initial Stop Loss value.",
        ),
        FieldDeclaration(
            name="real_tp",
            type=FieldType.decimal,
            nullable=False,
            description="Stores the position's current Take Profit value.",
        ),
        FieldDeclaration(
            name="real_sl",
            type=FieldType.decimal,
            nullable=False,
            description="Stores the position's current Stop Loss value.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the position is active.",
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the position.",
        ),
    ),
    primary_key="id",
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
        Relation(
            local_field="trading_platform_id", target_entity="Trading Platform", target_field="id"
        ),
        Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
        Relation(local_field="account_id", target_entity="Account", target_field="id"),
        Relation(
            local_field="trailing_group_id", target_entity="Trailing Group", target_field="id"
        ),
        Relation(local_field="partial_group_id", target_entity="Partial Group", target_field="id"),
        Relation(local_field="action_group_id", target_entity="Action Group", target_field="id"),
        Relation(local_field="action_id", target_entity="Action", target_field="id"),
    ),
    unique_constraints=(UniqueConstraint(fields=("name",)),),
)


class Position(Foundation, table=True):
    """Position."""

    __tablename__ = "Position"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

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
