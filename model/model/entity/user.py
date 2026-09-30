"""The User Entity."""

from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration
from model.core.foundation import Foundation


class User(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="User",
        description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                description="The user's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="username",
                description="The username used to identify the user.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="password",
                description="The password credential used by the user.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="api_key",
                description="The API key assigned to the user.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the user is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the user.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        unique_constraints=(
            ("name",),
            ("username",),
        ),
    )

    id: int | None = None
    name: str
    username: str
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None
