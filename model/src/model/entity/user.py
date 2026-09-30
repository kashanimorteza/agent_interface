"""The User Entity."""

from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Sensitivity,
    ValueGeneration,
)


class User(EntityBase):
    """The User Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="User",
        description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                description="The user's display name.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="username",
                description="The username used to identify the user.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="password",
                description="The password credential used by the user.",
                type=FieldType.STRING,
                nullable=False,
                sensitivity=Sensitivity.PASSWORD,
            ),
            FieldDeclaration(
                name="api_key",
                description="The API key assigned to the user.",
                type=FieldType.STRING,
                nullable=False,
                sensitivity=Sensitivity.SENSITIVE,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the user is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the user.",
                type=FieldType.STRING,
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
