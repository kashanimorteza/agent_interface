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


class PartialRule(Foundation, table=True):
    """Defines an individual Partial Close rule that tells the system under which condition
    part of an open position must be closed and how much of its volume must be closed.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="PartialRule",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("partial_group_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("profit_percentage", FieldType.DECIMAL, nullable=False),
            FieldDeclaration("close_percentage", FieldType.DECIMAL, nullable=False),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(
            UniqueConstraint(("name",)),
            UniqueConstraint(("partial_group_id", "profit_percentage")),
        ),
        references=(Reference(("partial_group_id",), "PartialGroup", ("id",)),),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the partial rule, assigned automatically.",
    )
    name: str = Field(description="The partial rule's display name.")
    partial_group_id: int = Field(
        description="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = Field(
        description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = Field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the partial rule is active."
    )
    description: str | None = Field(
        default=None, description="Describes the partial rule."
    )
