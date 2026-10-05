from decimal import Decimal
from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Trailing Rule",
    description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
    fields=(
        identity(),
        FieldDeclaration(
            name="name",
            description="The trailing rule's display name.",
            type=FieldType.STRING,
            nullable=False,
        ),
        FieldDeclaration(
            name="trailing_group_id",
            description="Identifies the trailing group that contains the rule.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="trigger_percentage",
            description="Defines the profit percentage of the take-profit target that activates the rule.",
            type=FieldType.DECIMAL,
            nullable=False,
        ),
        FieldDeclaration(
            name="take_profit_adjustment",
            description="Defines the take-profit adjustment applied when the rule is activated.",
            type=FieldType.DECIMAL,
            nullable=True,
        ),
        FieldDeclaration(
            name="stop_loss_adjustment",
            description="Defines the stop-loss adjustment applied when the rule is activated.",
            type=FieldType.DECIMAL,
            nullable=True,
        ),
        activity("Indicates whether the trailing rule is active."),
        FieldDeclaration(
            name="description",
            description="Describes the trailing rule.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(RelationDeclaration("trailing_group_id", "Trailing Group", "id"),),
    unique_constraints=(
        UniqueConstraintDeclaration(("name",)),
        UniqueConstraintDeclaration(
            (
                "trailing_group_id",
                "trigger_percentage",
            )
        ),
    ),
)


class TrailingRule(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    trailing_group_id: int = column(_DECLARATION, "trailing_group_id")
    trigger_percentage: Decimal = column(_DECLARATION, "trigger_percentage")
    take_profit_adjustment: Decimal | None = column(
        _DECLARATION, "take_profit_adjustment"
    )
    stop_loss_adjustment: Decimal | None = column(_DECLARATION, "stop_loss_adjustment")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
