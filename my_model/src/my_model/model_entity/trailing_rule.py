"""The Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class TrailingRule(Model_Foundation, table=True):
    """An individual rule within a Trailing Group defining when and how to manage Take Profit and Stop Loss."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="TrailingRule",
        purpose="An individual rule within a Trailing Group defining when and how to manage Take Profit and Stop Loss.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The trailing rule's display name.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the trailing group that contains the rule.",
            ),
            FieldDeclaration(
                name="trigger_percentage",
                type="decimal",
                nullable=False,
                purpose="The profit percentage of the take-profit target that activates the rule.",
            ),
            FieldDeclaration(
                name="take_profit_adjustment",
                type="decimal",
                nullable=True,
                purpose="The take-profit adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                name="stop_loss_adjustment",
                type="decimal",
                nullable=True,
                purpose="The stop-loss adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the trailing rule is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the trailing rule.",
            ),
        ),
        references=(
            ReferenceDeclaration(field="trailing_group_id", entity="TrailingGroup"),
        ),
        unique_constraints=(
            ("name",),
            ("trailing_group_id", "trigger_percentage"),
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
