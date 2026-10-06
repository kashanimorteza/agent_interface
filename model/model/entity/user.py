"""The User Entity."""

from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="User",
    description=(
        "Defines an independent user of the system and enables multi-user "
        "operation. Each user can have a separate set of settings, allowing "
        "new users to be added with configurations that remain distinct from "
        "those of existing users."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The user's display name.",
        ),
        FieldDeclaration(
            name="username",
            type=FieldType.string,
            nullable=False,
            description="The username used to identify the user.",
        ),
        FieldDeclaration(
            name="password",
            type=FieldType.string,
            nullable=False,
            description="The password credential used by the user.",
        ),
        FieldDeclaration(
            name="api_key",
            type=FieldType.string,
            nullable=False,
            description="The API key assigned to the user.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the user is active.",
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
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


class User(Foundation, table=True):
    """User."""

    __tablename__ = "User"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    username: str = column(_DECLARATION, "username")
    password: str = column(_DECLARATION, "password")
    api_key: str = column(_DECLARATION, "api_key")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
