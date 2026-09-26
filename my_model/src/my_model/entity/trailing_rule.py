"""Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class TrailingRule(ModelFoundation, table=True):
    """Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="TrailingRule",
        purpose="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The trailing rule's display name"
            ),
            FieldDeclaration(
                "trailing_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the trailing group that contains the rule",
            ),
            FieldDeclaration(
                "trigger_percentage",
                LogicalType.DECIMAL,
                purpose="Defines the profit percentage of the take-profit target that activates the rule",
            ),
            FieldDeclaration(
                "take_profit_adjustment",
                LogicalType.DECIMAL,
                nullable=True,
                purpose="Defines the take-profit adjustment applied when the rule is activated",
            ),
            FieldDeclaration(
                "stop_loss_adjustment",
                LogicalType.DECIMAL,
                nullable=True,
                purpose="Defines the stop-loss adjustment applied when the rule is activated",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the trailing rule is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the trailing rule",
            ),
        ),
        references=(
            Reference(
                "trailing_group_id", "TrailingGroup", "id", RelationshipKind.BELONGS_TO
            ),
        ),
        unique_constraints=(
            UniquenessConstraint(("name",)),
            UniquenessConstraint(
                (
                    "trailing_group_id",
                    "trigger_percentage",
                )
            ),
        ),
    )
    __table_args__ = (UniqueConstraint("trailing_group_id", "trigger_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    trailing_group_id: int = Field(foreign_key="trailinggroup.id")
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None
