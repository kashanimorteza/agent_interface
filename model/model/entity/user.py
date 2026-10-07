"""User Entity."""

from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="User",
    description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
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
        UniquenessConstraint(fields=("name",)),
        UniquenessConstraint(fields=("username",)),
    ),
)


class User(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    username: str = realize_field(DECLARATION, "username")
    password: str = realize_field(DECLARATION, "password")
    api_key: str = realize_field(DECLARATION, "api_key")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
