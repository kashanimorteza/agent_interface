"""The User Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)
from model.core.foundation import Foundation


class User(Foundation, table=True):
    __tablename__ = "User"
    declaration: ClassVar[Declaration] = Declaration(
        name="User",
        description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "name", FieldType.string, False, description="The user's display name."
            ),
            FieldDeclaration(
                "username",
                FieldType.string,
                False,
                description="The username used to identify the user.",
            ),
            FieldDeclaration(
                "password",
                FieldType.string,
                False,
                description="The password credential used by the user.",
            ),
            FieldDeclaration(
                "api_key",
                FieldType.string,
                False,
                description="The API key assigned to the user.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the user is active.",
                default=True,
            ),
            FieldDeclaration(
                "description", FieldType.string, True, description="Describes the user."
            ),
        ),
        primary_key="id",
        unique_constraints=(
            ("name",),
            ("username",),
        ),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    name: str = realize_field(declaration, "name")
    username: str = realize_field(declaration, "username")
    password: str = realize_field(declaration, "password")
    api_key: str = realize_field(declaration, "api_key")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
