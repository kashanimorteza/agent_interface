"""Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class PartialRule(ModelFoundation, table=True):
    """Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="PartialRule",
        purpose="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The partial rule's display name"
            ),
            FieldDeclaration(
                "partial_group_id",
                LogicalType.INTEGER,
                purpose="Identifies the partial group that contains the rule",
            ),
            FieldDeclaration(
                "profit_percentage",
                LogicalType.DECIMAL,
                purpose="Defines the profit percentage that activates the rule",
            ),
            FieldDeclaration(
                "close_percentage",
                LogicalType.DECIMAL,
                purpose="Defines the percentage of the position closed when the rule is activated",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the partial rule is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the partial rule",
            ),
        ),
        references=(
            Reference(
                "partial_group_id", "PartialGroup", "id", RelationshipKind.BELONGS_TO
            ),
        ),
        unique_constraints=(
            UniquenessConstraint(("name",)),
            UniquenessConstraint(
                (
                    "partial_group_id",
                    "profit_percentage",
                )
            ),
        ),
    )
    __table_args__ = (UniqueConstraint("partial_group_id", "profit_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    partial_group_id: int = Field(foreign_key="partialgroup.id")
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
