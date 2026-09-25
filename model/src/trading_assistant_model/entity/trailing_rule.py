from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class TrailingRule(Foundation, table=True):
    """Defines an individual rule within a Trailing Group that tells the system when and
    how to manage Take Profit and Stop Loss. Each rule provides the activation condition
    and the parameters used to apply the required adjustments.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="TrailingRule",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("trailing_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("trigger_percentage", FieldType.DECIMAL, nullable=False),
            FieldDeclaration(
                "take_profit_adjustment", FieldType.DECIMAL, nullable=True
            ),
            FieldDeclaration("stop_loss_adjustment", FieldType.DECIMAL, nullable=True),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(
            UniqueConstraint(("name",)),
            UniqueConstraint(("trailing_group_id", "trigger_percentage")),
        ),
        references=(Reference(("trailing_group_id",), "TrailingGroup", ("id",)),),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the trailing rule, assigned automatically.",
    )
    name: str = Field(description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = Field(
        description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the trailing rule is active."
    )
    description: str | None = Field(
        default=None, description="Describes the trailing rule."
    )
