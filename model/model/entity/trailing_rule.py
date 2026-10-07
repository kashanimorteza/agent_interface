"""Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

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
    name="Trailing Rule",
    description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
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
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The trailing rule's display name.",
        ),
        FieldDeclaration(
            name="trailing_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the trailing group that contains the rule.",
        ),
        FieldDeclaration(
            name="trigger_percentage",
            type=FieldType.decimal,
            nullable=False,
            description="Defines the profit percentage of the take-profit target that activates the rule.",
        ),
        FieldDeclaration(
            name="take_profit_adjustment",
            type=FieldType.decimal,
            nullable=True,
            description="Defines the take-profit adjustment applied when the rule is activated.",
        ),
        FieldDeclaration(
            name="stop_loss_adjustment",
            type=FieldType.decimal,
            nullable=True,
            description="Defines the stop-loss adjustment applied when the rule is activated.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the trailing rule is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the trailing rule.",
        ),
    ),
    primary_key="id",
    relations=(
        Relation(
            local_field="trailing_group_id",
            target_entity="Trailing Group",
            target_field="id",
        ),
    ),
    unique_constraints=(
        UniquenessConstraint(fields=("name",)),
        UniquenessConstraint(fields=("trailing_group_id", "trigger_percentage")),
    ),
)


class TrailingRule(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    trailing_group_id: int = realize_field(DECLARATION, "trailing_group_id")
    trigger_percentage: Decimal = realize_field(DECLARATION, "trigger_percentage")
    take_profit_adjustment: Decimal | None = realize_field(
        DECLARATION, "take_profit_adjustment"
    )
    stop_loss_adjustment: Decimal | None = realize_field(
        DECLARATION, "stop_loss_adjustment"
    )
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
