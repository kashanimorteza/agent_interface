"""The Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)


class PartialRule(EntityBase):
    """The Partial Rule Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Rule",
        description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                description="The partial rule's display name.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="partial_group_id",
                description="Identifies the partial group that contains the rule.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="profit_percentage",
                description="Defines the profit percentage that activates the rule.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="close_percentage",
                description="Defines the percentage of the position closed when the rule is activated.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the partial rule is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the partial rule.",
                type=FieldType.STRING,
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(Relation("partial_group_id", "Partial Group", "id"),),
        unique_constraints=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
    )

    id: int | None = None
    name: str
    partial_group_id: int
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
