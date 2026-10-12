"""The Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

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


class TrailingRule(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Rule",
        description=(
            "Defines an individual rule within a Trailing Group that tells the system when and "
            "how to manage Take Profit and Stop Loss. Each rule provides the activation "
            "condition and the parameters used to apply the required adjustments."
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
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The trailing rule's display name.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the trailing group that contains the rule.",
            ),
            FieldDeclaration(
                name="trigger_percentage",
                type=FieldType.DECIMAL,
                nullable=False,
                description=(
                    "Defines the profit percentage of the take-profit target that activates "
                    "the rule."
                ),
            ),
            FieldDeclaration(
                name="take_profit_adjustment",
                type=FieldType.DECIMAL,
                nullable=True,
                description="Defines the take-profit adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                name="stop_loss_adjustment",
                type=FieldType.DECIMAL,
                nullable=True,
                description="Defines the stop-loss adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the trailing rule is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the trailing rule.",
            ),
        ),
        relations=(Relation("trailing_group_id", "Trailing Group", "id"),),
        unique_constraints=(
            UniquenessConstraint(("name",)),
            UniquenessConstraint(("trailing_group_id", "trigger_percentage")),
        ),
    )

    __tablename__ = "TrailingRule"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    name: str = mapped_field(declaration, "name")
    trailing_group_id: int = mapped_field(declaration, "trailing_group_id")
    trigger_percentage: Decimal = mapped_field(declaration, "trigger_percentage")
    take_profit_adjustment: Decimal | None = mapped_field(
        declaration, "take_profit_adjustment"
    )
    stop_loss_adjustment: Decimal | None = mapped_field(
        declaration, "stop_loss_adjustment"
    )
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
