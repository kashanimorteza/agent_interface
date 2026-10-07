"""Partial Rule Entity."""

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
    name="Partial Rule",
    description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
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
            description="The partial rule's display name.",
        ),
        FieldDeclaration(
            name="partial_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the partial group that contains the rule.",
        ),
        FieldDeclaration(
            name="profit_percentage",
            type=FieldType.decimal,
            nullable=False,
            description="Defines the profit percentage that activates the rule.",
        ),
        FieldDeclaration(
            name="close_percentage",
            type=FieldType.decimal,
            nullable=False,
            description="Defines the percentage of the position closed when the rule is activated.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the partial rule is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the partial rule.",
        ),
    ),
    primary_key="id",
    relations=(
        Relation(
            local_field="partial_group_id",
            target_entity="Partial Group",
            target_field="id",
        ),
    ),
    unique_constraints=(
        UniquenessConstraint(fields=("name",)),
        UniquenessConstraint(fields=("partial_group_id", "profit_percentage")),
    ),
)


class PartialRule(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    partial_group_id: int = realize_field(DECLARATION, "partial_group_id")
    profit_percentage: Decimal = realize_field(DECLARATION, "profit_percentage")
    close_percentage: Decimal = realize_field(DECLARATION, "close_percentage")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
