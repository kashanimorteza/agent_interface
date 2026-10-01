"""The Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Partial Rule",
    description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
            type="integer",
            nullable=False,
            immutable=True,
            value_generation="auto_increment",
        ),
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
        FieldDeclaration(
            name="is_active",
            description="Indicates whether the partial rule is active.",
            type="boolean",
            nullable=False,
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            description="Describes the partial rule.",
            type="string",
            nullable=True,
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
        ("name",),
        ("partial_group_id", "profit_percentage"),
    ),
    indexes=(),
)


class PartialRule(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    name: str = Field(
        description="The partial rule's display name.",
        **column_options(_DECLARATION, "name"),
    )
    partial_group_id: int = Field(
        description="Identifies the partial group that contains the rule.",
        **column_options(_DECLARATION, "partial_group_id"),
    )
    profit_percentage: Decimal = Field(
        description="Defines the profit percentage that activates the rule.",
        **column_options(_DECLARATION, "profit_percentage"),
    )
    close_percentage: Decimal = Field(
        description="Defines the percentage of the position closed when the rule is activated.",
        **column_options(_DECLARATION, "close_percentage"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the partial rule is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the partial rule.",
        **column_options(_DECLARATION, "description"),
    )
