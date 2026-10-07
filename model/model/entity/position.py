"""Position Entity."""

from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Position",
    description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
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
            default=Decimal(0),
        ),
        FieldDeclaration(
            name="is_executed",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the position has been executed.",
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
    unique_constraints=(UniquenessConstraint(fields=("name",)),),
)


class Position(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    user_id: int = realize_field(DECLARATION, "user_id")
    name: str = realize_field(DECLARATION, "name")
    trading_platform_id: int = realize_field(DECLARATION, "trading_platform_id")
    broker_id: int = realize_field(DECLARATION, "broker_id")
    account_id: int = realize_field(DECLARATION, "account_id")
    trailing_group_id: int = realize_field(DECLARATION, "trailing_group_id")
    partial_group_id: int = realize_field(DECLARATION, "partial_group_id")
    action_group_id: int = realize_field(DECLARATION, "action_group_id")
    action_id: int = realize_field(DECLARATION, "action_id")
    date: AwareDatetime = realize_field(DECLARATION, "date")
    volume: Decimal = realize_field(DECLARATION, "volume")
    profit: Decimal = realize_field(DECLARATION, "profit")
    is_executed: bool = realize_field(DECLARATION, "is_executed")
    order_type: str = realize_field(DECLARATION, "order_type")
    base_tp: Decimal = realize_field(DECLARATION, "base_tp")
    base_sl: Decimal = realize_field(DECLARATION, "base_sl")
    real_tp: Decimal = realize_field(DECLARATION, "real_tp")
    real_sl: Decimal = realize_field(DECLARATION, "real_sl")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
