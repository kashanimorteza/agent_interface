"""Broker Domain Entity."""

from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    ReferenceDeclaration,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Broker(ModelFoundation, table=True):
    """Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Broker",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("user_id", LogicalType.INTEGER),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(ReferenceDeclaration("user_id", "User"),),
        unique_constraints=(("user_id", "name"),),
    )

    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str
    user_id: int = Field(foreign_key="user.id")
    is_active: bool = True
    description: str | None = None
