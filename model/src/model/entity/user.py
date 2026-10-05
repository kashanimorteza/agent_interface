from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="User",
    description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
    fields=(
        identity(),
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
        ),
        FieldDeclaration(
            name="api_key",
            description="The API key assigned to the user.",
            type=FieldType.STRING,
            nullable=False,
        ),
        activity("Indicates whether the user is active."),
        FieldDeclaration(
            name="description",
            description="Describes the user.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    unique_constraints=(
        UniqueConstraintDeclaration(("name",)),
        UniqueConstraintDeclaration(("username",)),
    ),
)


class User(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    username: str = column(_DECLARATION, "username")
    password: str = column(_DECLARATION, "password")
    api_key: str = column(_DECLARATION, "api_key")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
