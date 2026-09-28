"""The User Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraint,
    ValueGeneration,
)


class User(Entity, table=True):
    """The User Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="User",
        description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
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
                description="The user's display name.",
            ),
            FieldDeclaration(
                name="username",
                type=FieldType.STRING,
                nullable=False,
                description="The username used to identify the user.",
            ),
            FieldDeclaration(
                name="password",
                type=FieldType.STRING,
                nullable=False,
                description="The password credential used by the user.",
            ),
            FieldDeclaration(
                name="api_key",
                type=FieldType.STRING,
                nullable=False,
                description="The API key assigned to the user.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the user is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the user.",
            ),
        ),
        primary_key="id",
        unique_constraints=(
            UniqueConstraint(fields=("name",)),
            UniqueConstraint(fields=("username",)),
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None
