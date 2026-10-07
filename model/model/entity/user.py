"""The User Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    Sensitivity,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="User",
    description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The user's display name.",
        ),
        FieldDeclaration(
            "username",
            FieldType.string,
            nullable=False,
            description="The username used to identify the user.",
        ),
        FieldDeclaration(
            "password",
            FieldType.string,
            nullable=False,
            description="The password credential used by the user.",
            sensitivity=Sensitivity.password,
        ),
        FieldDeclaration(
            "api_key",
            FieldType.string,
            nullable=False,
            description="The API key assigned to the user.",
            sensitivity=Sensitivity.sensitive,
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the user is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the user.",
        ),
    ),
    unique_constraints=(
        UniqueConstraint(("name",)),
        UniqueConstraint(("username",)),
    ),
)


class User(Foundation, table=True):
    __tablename__ = "User"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    username: str = realize_field(DECLARATION, "username")
    password: str = realize_field(DECLARATION, "password")
    api_key: str = realize_field(DECLARATION, "api_key")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
