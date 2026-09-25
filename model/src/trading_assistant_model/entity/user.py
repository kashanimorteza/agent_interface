from typing import ClassVar

from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class User(Foundation, table=True):
    """Defines an independent user of the system and enables multi-user operation. Each
    user can have a separate set of settings, allowing new users to be added with
    configurations that remain distinct from those of existing users.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="User",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("username", FieldType.STRING, nullable=False),
            FieldDeclaration(
                "password", FieldType.STRING, nullable=False, sensitive=True
            ),
            FieldDeclaration(
                "api_key", FieldType.STRING, nullable=False, sensitive=True
            ),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(
            UniqueConstraint(("name",)),
            UniqueConstraint(("username",)),
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the user, assigned automatically.",
    )
    name: str = Field(description="The user's display name.")
    username: str = Field(description="The username used to identify the user.")
    password: str = Field(description="The password credential used by the user.")
    api_key: str = Field(description="The API key assigned to the user.")
    is_active: bool = Field(
        default=True, description="Indicates whether the user is active."
    )
    description: str | None = Field(default=None, description="Describes the user.")
