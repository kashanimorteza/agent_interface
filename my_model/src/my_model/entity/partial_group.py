"""Partial Group Entity."""

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


class PartialGroup(ModelFoundation, table=True):
    """Defines an independent group of rules for managing portions of an open trade."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="PartialGroup",
        purpose="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "user_id",
                LogicalType.INTEGER,
                purpose="Identifies the user who owns the partial group",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The partial group's display name"
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the partial group is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the partial group",
            ),
        ),
        references=(Reference("user_id", "User", "id", RelationshipKind.BELONGS_TO),),
        unique_constraints=(
            UniquenessConstraint(
                (
                    "user_id",
                    "name",
                )
            ),
        ),
    )
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    is_active: bool = True
    description: str | None = None
