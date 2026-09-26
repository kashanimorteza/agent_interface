"""Broker Entity."""

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


class Broker(ModelFoundation, table=True):
    """Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Broker",
        purpose="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The broker's display name"
            ),
            FieldDeclaration(
                "user_id",
                LogicalType.INTEGER,
                purpose="Identifies the user who owns the broker configuration",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the broker is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the broker",
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
    name: str
    user_id: int = Field(foreign_key="user.id")
    is_active: bool = True
    description: str | None = None
