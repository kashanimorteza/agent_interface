from decimal import Decimal
from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core._columns import DecimalText
from model.core.declaration import Declaration, FieldDeclaration, Relation


class TrailingRule(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("trailing_group_id", "trigger_percentage"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Trailing Rule",
        "Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("name", "The trailing rule's display name.", "string", False),
            FieldDeclaration(
                "trailing_group_id", "Identifies the trailing group that contains the rule.", "integer", False
            ),
            FieldDeclaration(
                "trigger_percentage",
                "Defines the profit percentage of the take-profit target that activates the rule.",
                "decimal",
                False,
            ),
            FieldDeclaration(
                "take_profit_adjustment",
                "Defines the take-profit adjustment applied when the rule is activated.",
                "decimal",
                True,
            ),
            FieldDeclaration(
                "stop_loss_adjustment",
                "Defines the stop-loss adjustment applied when the rule is activated.",
                "decimal",
                True,
            ),
            FieldDeclaration(
                "is_active",
                "Indicates whether the trailing rule is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the trailing rule.", "string", True),
        ),
        "id",
        relations=(Relation("trailing_group_id", "Trailing Group", "id"),),
        unique_constraints=(
            ("name",),
            (
                "trailing_group_id",
                "trigger_percentage",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    name: str = Field(unique=True, description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        foreign_key="TrailingGroup.id", description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = Field(
        sa_type=DecimalText,
        description="Defines the profit percentage of the take-profit target that activates the rule.",
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        sa_type=DecimalText,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        sa_type=DecimalText,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = Field(default=True, description="Indicates whether the trailing rule is active.")
    description: str | None = Field(default=None, description="Describes the trailing rule.")
