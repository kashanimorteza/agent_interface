"""User Domain Entity."""

from typing import ClassVar

from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class User(ModelFoundation, table=True):
    """Defines an independent user of the system and enables multi-user operation."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="User",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("username", LogicalType.STRING),
            FieldDeclaration("password", LogicalType.STRING, sensitive=True),
            FieldDeclaration("api_key", LogicalType.STRING, sensitive=True),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(),
        unique_constraints=(
            ("name",),
            ("username",),
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None
