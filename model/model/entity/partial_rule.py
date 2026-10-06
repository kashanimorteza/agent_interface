"""The Partial Rule Entity."""

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
    name="Partial Rule",
    description=(
        "Defines an individual Partial Close rule that tells the system under "
        "which condition part of an open position must be closed and how much "
        "of its volume must be closed."
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
            description=(
                "Defines the percentage of the position closed when the rule is activated."
            ),
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the partial rule is active.",
            has_default=True,
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
        Relation(local_field="partial_group_id", target_entity="Partial Group", target_field="id"),
    ),
    unique_constraints=(
        UniqueConstraint(fields=("name",)),
        UniqueConstraint(fields=("partial_group_id", "profit_percentage")),
    ),
)


class PartialRule(Foundation, table=True):
    """Partial Rule."""

    __tablename__ = "PartialRule"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    partial_group_id: int = column(_DECLARATION, "partial_group_id")
    profit_percentage: Decimal = column(_DECLARATION, "profit_percentage")
    close_percentage: Decimal = column(_DECLARATION, "close_percentage")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
