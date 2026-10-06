"""The Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Trailing Rule",
    description=(
        "Defines an individual rule within a Trailing Group that tells the "
        "system when and how to manage Take Profit and Stop Loss. Each rule "
        "provides the activation condition and the parameters used to apply "
        "the required adjustments."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
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
            description=(
                "Defines the profit percentage of the take-profit target that activates the rule."
            ),
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
            has_default=True,
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
            local_field="trailing_group_id", target_entity="Trailing Group", target_field="id"
        ),
    ),
    unique_constraints=(
        UniqueConstraint(fields=("name",)),
        UniqueConstraint(fields=("trailing_group_id", "trigger_percentage")),
    ),
)


class TrailingRule(Foundation, table=True):
    """Trailing Rule."""

    __tablename__ = "TrailingRule"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    trailing_group_id: int = column(_DECLARATION, "trailing_group_id")
    trigger_percentage: Decimal = column(_DECLARATION, "trigger_percentage")
    take_profit_adjustment: Decimal | None = column(_DECLARATION, "take_profit_adjustment")
    stop_loss_adjustment: Decimal | None = column(_DECLARATION, "stop_loss_adjustment")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
