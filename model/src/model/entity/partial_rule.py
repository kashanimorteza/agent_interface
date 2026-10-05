from decimal import Decimal
from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Partial Rule",
    description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
    fields=(
        identity(),
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
        activity("Indicates whether the partial rule is active."),
        FieldDeclaration(
            name="description",
            description="Describes the partial rule.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(RelationDeclaration("partial_group_id", "Partial Group", "id"),),
    unique_constraints=(
        UniqueConstraintDeclaration(("name",)),
        UniqueConstraintDeclaration(
            (
                "partial_group_id",
                "profit_percentage",
            )
        ),
    ),
)


class PartialRule(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    partial_group_id: int = column(_DECLARATION, "partial_group_id")
    profit_percentage: Decimal = column(_DECLARATION, "profit_percentage")
    close_percentage: Decimal = column(_DECLARATION, "close_percentage")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
