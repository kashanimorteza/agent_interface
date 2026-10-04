"""The Partial Rule Entity."""

from decimal import Decimal

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import DecimalText, table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class PartialRule(Entity, table=True):
    """The Partial Rule Entity."""

    __tablename__ = "PartialRule"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("partial_group_id", "profit_percentage"),
    )

    declaration = Declaration(
        name="Partial Rule",
        description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="name",
                description="The partial rule's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="partial_group_id",
                description="Identifies the partial group that contains the rule.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="profit_percentage",
                description="Defines the profit percentage that activates the rule.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="close_percentage",
                description="Defines the percentage of the position closed when the rule is activated.",
                type="decimal",
                nullable=False,
            ),
            activity_declaration("Indicates whether the partial rule is active."),
            FieldDeclaration(
                name="description",
                description="Describes the partial rule.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="partial_group_id",
                target_entity="Partial Group",
                target_field="id",
            ),
        ),
        unique_constraints=(("name",), ("partial_group_id", "profit_percentage")),
    )

    id: int | None = identity_field()
    name: str = Field(unique=True, description="The partial rule's display name.")
    partial_group_id: int = Field(
        foreign_key="PartialGroup.id",
        description="Identifies the partial group that contains the rule.",
    )
    profit_percentage: Decimal = Field(
        sa_type=DecimalText,
        description="Defines the profit percentage that activates the rule.",
    )
    close_percentage: Decimal = Field(
        sa_type=DecimalText,
        description="Defines the percentage of the position closed when the rule is activated.",
    )
    is_active: bool = activity_field("Indicates whether the partial rule is active.")
    description: str | None = Field(
        default=None, description="Describes the partial rule."
    )
