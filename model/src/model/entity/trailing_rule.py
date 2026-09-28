"""The Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class TrailingRule(Entity, table=True):
    """The Trailing Rule Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Rule",
        description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
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
                description="Defines the profit percentage of the take-profit target that activates the rule.",
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
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
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
            UniqueConstraint(fields=("name",)),
            UniqueConstraint(fields=("trailing_group_id", "trigger_percentage")),
        ),
    )

    __table_args__ = (TableUniqueConstraint("trailing_group_id", "trigger_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    trailing_group_id: int
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None
