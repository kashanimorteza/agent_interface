"""The Position Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core._types import DecimalValue, Timestamp
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class Position(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Position",
        description=(
            "Stores the complete information for every position "
            "created by the system. It allows the system to "
            "identify and track positions that have been opened "
            "as well as positions that are still pending "
            "execution."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description="Identifies the user who owns the position.",
            ),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The position's display name.",
            ),
            FieldDeclaration(
                "trading_platform_id",
                "integer",
                nullable=False,
                description=(
                    "Identifies the trading platform used to execute the position."
                ),
            ),
            FieldDeclaration(
                "broker_id",
                "integer",
                nullable=False,
                description=(
                    "Identifies the broker through which the position is executed."
                ),
            ),
            FieldDeclaration(
                "account_id",
                "integer",
                nullable=False,
                description=("Identifies the trading account used for the position."),
            ),
            FieldDeclaration(
                "trailing_group_id",
                "integer",
                nullable=False,
                description=("Identifies the Trailing Group applied to the position."),
            ),
            FieldDeclaration(
                "partial_group_id",
                "integer",
                nullable=False,
                description=("Identifies the Partial Group applied to the position."),
            ),
            FieldDeclaration(
                "action_group_id",
                "integer",
                nullable=False,
                description=(
                    "Identifies the Action Group associated with the position."
                ),
            ),
            FieldDeclaration(
                "action_id",
                "integer",
                nullable=False,
                description=(
                    "Identifies the action from which the position is created."
                ),
            ),
            FieldDeclaration(
                "date",
                "datetime",
                nullable=False,
                description="Stores the position's date and time.",
            ),
            FieldDeclaration(
                "volume",
                "decimal",
                nullable=False,
                description="Stores the position's trading volume.",
            ),
            FieldDeclaration(
                "profit",
                "decimal",
                nullable=False,
                description="Stores the position's current profit or loss.",
                has_default=True,
                default=Decimal("0"),
            ),
            FieldDeclaration(
                "is_executed",
                "boolean",
                nullable=False,
                description="Indicates whether the position has been executed.",
                has_default=True,
                default=False,
            ),
            FieldDeclaration(
                "order_type",
                "string",
                nullable=False,
                description="Stores the position's order type.",
            ),
            FieldDeclaration(
                "base_tp",
                "decimal",
                nullable=False,
                description="Stores the position's initial Take Profit value.",
            ),
            FieldDeclaration(
                "base_sl",
                "decimal",
                nullable=False,
                description="Stores the position's initial Stop Loss value.",
            ),
            FieldDeclaration(
                "real_tp",
                "decimal",
                nullable=False,
                description="Stores the position's current Take Profit value.",
            ),
            FieldDeclaration(
                "real_sl",
                "decimal",
                nullable=False,
                description="Stores the position's current Stop Loss value.",
            ),
            activity("Indicates whether the position is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the position.",
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
    date: Timestamp
    volume: DecimalValue
    profit: DecimalValue = Decimal("0")
    is_executed: bool = False
    order_type: str
    base_tp: DecimalValue
    base_sl: DecimalValue
    real_tp: DecimalValue
    real_sl: DecimalValue
    is_active: bool = True
    description: str | None = None
