"""The Partial Rule Entity."""

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


class PartialRule(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Rule",
        description=(
            "Defines an individual Partial Close rule that tells the system under which "
            "condition part of an open position must be closed and how much of its volume must "
            "be closed."
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
                description="The partial rule's display name.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the partial group that contains the rule.",
            ),
            FieldDeclaration(
                name="profit_percentage",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Defines the profit percentage that activates the rule.",
            ),
            FieldDeclaration(
                name="close_percentage",
                type=FieldType.DECIMAL,
                nullable=False,
                description=(
                    "Defines the percentage of the position closed when the rule is activated."
                ),
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the partial rule is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the partial rule.",
            ),
        ),
        relations=(Relation("partial_group_id", "Partial Group", "id"),),
        unique_constraints=(
            UniquenessConstraint(("name",)),
            UniquenessConstraint(("partial_group_id", "profit_percentage")),
        ),
    )

    __tablename__ = "PartialRule"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    name: str = mapped_field(declaration, "name")
    partial_group_id: int = mapped_field(declaration, "partial_group_id")
    profit_percentage: Decimal = mapped_field(declaration, "profit_percentage")
    close_percentage: Decimal = mapped_field(declaration, "close_percentage")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
