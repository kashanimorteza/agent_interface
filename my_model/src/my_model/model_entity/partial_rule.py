"""The Partial Rule Entity."""

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


class PartialRule(Model_Foundation, table=True):
    """An individual Partial Close rule defining when and how much of an open position is closed."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="PartialRule",
        purpose="An individual Partial Close rule defining when and how much of an open position is closed.",
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
                purpose="The partial rule's display name.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the partial group that contains the rule.",
            ),
            FieldDeclaration(
                name="profit_percentage",
                type="decimal",
                nullable=False,
                purpose="The profit percentage that activates the rule.",
            ),
            FieldDeclaration(
                name="close_percentage",
                type="decimal",
                nullable=False,
                purpose="The percentage of the position closed when the rule is activated.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the partial rule is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the partial rule.",
            ),
        ),
        references=(
            ReferenceDeclaration(field="partial_group_id", entity="PartialGroup"),
        ),
        unique_constraints=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
    )
    __table_args__ = (UniqueConstraint("partial_group_id", "profit_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    partial_group_id: int = Field(foreign_key="partialgroup.id")
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
