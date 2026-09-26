"""Partial Group Domain Entity."""

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


class PartialGroup(ModelFoundation, table=True):
    """Defines an independent group of rules for managing portions of an open trade."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Partial Group",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", LogicalType.INTEGER),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(ReferenceDeclaration("user_id", "User"),),
        unique_constraints=(("user_id", "name"),),
    )

    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    is_active: bool = True
    description: str | None = None
