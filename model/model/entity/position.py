"""The Position Entity."""

from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Position",
    description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "user_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the user who owns the position.",
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The position's display name.",
        ),
        FieldDeclaration(
            "trading_platform_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the trading platform used to execute the position.",
        ),
        FieldDeclaration(
            "broker_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the broker through which the position is executed.",
        ),
        FieldDeclaration(
            "account_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the trading account used for the position.",
        ),
        FieldDeclaration(
            "trailing_group_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the Trailing Group applied to the position.",
        ),
        FieldDeclaration(
            "partial_group_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the Partial Group applied to the position.",
        ),
        FieldDeclaration(
            "action_group_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the Action Group associated with the position.",
        ),
        FieldDeclaration(
            "action_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the action from which the position is created.",
        ),
        FieldDeclaration(
            "date",
            FieldType.datetime,
            nullable=False,
            description="Stores the position's date and time.",
        ),
        FieldDeclaration(
            "volume",
            FieldType.decimal,
            nullable=False,
            description="Stores the position's trading volume.",
        ),
        FieldDeclaration(
            "profit",
            FieldType.decimal,
            nullable=False,
            description="Stores the position's current profit or loss.",
            default=Decimal(0),
        ),
        FieldDeclaration(
            "is_executed",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the position has been executed.",
            default=False,
        ),
        FieldDeclaration(
            "order_type",
            FieldType.string,
            nullable=False,
            description="Stores the position's order type.",
        ),
        FieldDeclaration(
            "base_tp",
            FieldType.decimal,
            nullable=False,
            description="Stores the position's initial Take Profit value.",
        ),
        FieldDeclaration(
            "base_sl",
            FieldType.decimal,
            nullable=False,
            description="Stores the position's initial Stop Loss value.",
        ),
        FieldDeclaration(
            "real_tp",
            FieldType.decimal,
            nullable=False,
            description="Stores the position's current Take Profit value.",
        ),
        FieldDeclaration(
            "real_sl",
            FieldType.decimal,
            nullable=False,
            description="Stores the position's current Stop Loss value.",
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the position is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the position.",
        ),
    ),
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
    unique_constraints=(UniqueConstraint(("name",)),),
)


class Position(Foundation, table=True):
    __tablename__ = "Position"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

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
