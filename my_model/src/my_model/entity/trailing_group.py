"""Trailing Group Entity."""

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


class TrailingGroup(ModelFoundation, table=True):
    """Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="TrailingGroup",
        purpose="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
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
                purpose="Identifies the user who owns the trailing group",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The trailing group's display name"
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the trailing group is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the trailing group",
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
