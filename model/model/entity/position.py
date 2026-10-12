"""The Position Entity."""

from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Position(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Position",
        description=(
            "Stores the complete information for every position created by the system. It "
            "allows the system to identify and track positions that have been opened as well as "
            "positions that are still pending execution."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
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
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="is_executed",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the position has been executed.",
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
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
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
        unique_constraints=(UniquenessConstraint(("name",)),),
    )

    __tablename__ = "Position"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    user_id: int = mapped_field(declaration, "user_id")
    name: str = mapped_field(declaration, "name")
    trading_platform_id: int = mapped_field(declaration, "trading_platform_id")
    broker_id: int = mapped_field(declaration, "broker_id")
    account_id: int = mapped_field(declaration, "account_id")
    trailing_group_id: int = mapped_field(declaration, "trailing_group_id")
    partial_group_id: int = mapped_field(declaration, "partial_group_id")
    action_group_id: int = mapped_field(declaration, "action_group_id")
    action_id: int = mapped_field(declaration, "action_id")
    date: AwareDatetime = mapped_field(declaration, "date")
    volume: Decimal = mapped_field(declaration, "volume")
    profit: Decimal = mapped_field(declaration, "profit")
    is_executed: bool = mapped_field(declaration, "is_executed")
    order_type: str = mapped_field(declaration, "order_type")
    base_tp: Decimal = mapped_field(declaration, "base_tp")
    base_sl: Decimal = mapped_field(declaration, "base_sl")
    real_tp: Decimal = mapped_field(declaration, "real_tp")
    real_sl: Decimal = mapped_field(declaration, "real_sl")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
