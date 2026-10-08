"""Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class TrailingRule(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Rule",
        description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
        primary_key="id",
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
        relations=(
            Relation(
                local_field="trailing_group_id",
                target_entity="Trailing Group",
                target_field="id",
            ),
        ),
        unique_constraints=(
            ("name",),
            ("trailing_group_id", "trigger_percentage"),
        ),
    )
    __tablename__ = "TrailingRule"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    name: str = storage.field(declaration, "name")
    trailing_group_id: int = storage.field(declaration, "trailing_group_id")
    trigger_percentage: Decimal = storage.field(declaration, "trigger_percentage")
    take_profit_adjustment: Decimal | None = storage.field(
        declaration, "take_profit_adjustment"
    )
    stop_loss_adjustment: Decimal | None = storage.field(
        declaration, "stop_loss_adjustment"
    )
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
