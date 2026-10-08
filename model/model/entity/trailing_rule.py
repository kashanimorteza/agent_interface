"""The Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class TrailingRule(Foundation, table=True):
    __tablename__ = "TrailingRule"
    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Rule",
        description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "name",
                FieldType.string,
                False,
                description="The trailing rule's display name.",
            ),
            FieldDeclaration(
                "trailing_group_id",
                FieldType.integer,
                False,
                description="Identifies the trailing group that contains the rule.",
            ),
            FieldDeclaration(
                "trigger_percentage",
                FieldType.decimal,
                False,
                description="Defines the profit percentage of the take-profit target that activates the rule.",
            ),
            FieldDeclaration(
                "take_profit_adjustment",
                FieldType.decimal,
                True,
                description="Defines the take-profit adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                "stop_loss_adjustment",
                FieldType.decimal,
                True,
                description="Defines the stop-loss adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the trailing rule is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the trailing rule.",
            ),
        ),
        primary_key="id",
        relations=(Relation("trailing_group_id", "Trailing Group", "id"),),
        unique_constraints=(
            ("name",),
            ("trailing_group_id", "trigger_percentage"),
        ),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    name: str = realize_field(declaration, "name")
    trailing_group_id: int = realize_field(declaration, "trailing_group_id")
    trigger_percentage: Decimal = realize_field(declaration, "trigger_percentage")
    take_profit_adjustment: Decimal | None = realize_field(
        declaration, "take_profit_adjustment"
    )
    stop_loss_adjustment: Decimal | None = realize_field(
        declaration, "stop_loss_adjustment"
    )
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
