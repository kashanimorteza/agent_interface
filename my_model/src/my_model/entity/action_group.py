"""Action Group Entity."""

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


class ActionGroup(ModelFoundation, table=True):
    """Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="ActionGroup",
        purpose="Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.",
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
                purpose="Identifies the user who owns the action group",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The action group's display name"
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the action group is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the action group",
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
