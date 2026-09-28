"""The Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class PartialRule(Entity, table=True):
    """The Partial Rule Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Rule",
        description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
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
                description="Defines the percentage of the position closed when the rule is activated.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the partial rule is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
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
            UniqueConstraint(fields=("name",)),
            UniqueConstraint(fields=("partial_group_id", "profit_percentage")),
        ),
    )

    __table_args__ = (TableUniqueConstraint("partial_group_id", "profit_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    partial_group_id: int
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
