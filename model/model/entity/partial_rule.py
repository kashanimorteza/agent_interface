"""The Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Partial Rule",
    description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The partial rule's display name.",
        ),
        FieldDeclaration(
            "partial_group_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the partial group that contains the rule.",
        ),
        FieldDeclaration(
            "profit_percentage",
            FieldType.decimal,
            nullable=False,
            description="Defines the profit percentage that activates the rule.",
        ),
        FieldDeclaration(
            "close_percentage",
            FieldType.decimal,
            nullable=False,
            description="Defines the percentage of the position closed when the rule is activated.",
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the partial rule is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the partial rule.",
        ),
    ),
    relations=(Relation("partial_group_id", "Partial Group", "id"),),
    unique_constraints=(
        UniqueConstraint(("name",)),
        UniqueConstraint(("partial_group_id", "profit_percentage")),
    ),
)


class PartialRule(Foundation, table=True):
    __tablename__ = "PartialRule"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    partial_group_id: int = realize_field(DECLARATION, "partial_group_id")
    profit_percentage: Decimal = realize_field(DECLARATION, "profit_percentage")
    close_percentage: Decimal = realize_field(DECLARATION, "close_percentage")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
