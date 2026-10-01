"""The User Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="User",
    description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
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
            sensitivity="password",
        ),
        FieldDeclaration(
            name="api_key",
            description="The API key assigned to the user.",
            type="string",
            nullable=False,
            sensitivity="sensitive",
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
    relations=(),
    unique_constraints=(
        ("name",),
        ("username",),
    ),
    indexes=(),
)


class User(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    name: str = Field(
        description="The user's display name.", **column_options(_DECLARATION, "name")
    )
    username: str = Field(
        description="The username used to identify the user.",
        **column_options(_DECLARATION, "username"),
    )
    password: str = Field(
        description="The password credential used by the user.",
        **column_options(_DECLARATION, "password"),
    )
    api_key: str = Field(
        description="The API key assigned to the user.",
        **column_options(_DECLARATION, "api_key"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the user is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the user.",
        **column_options(_DECLARATION, "description"),
    )
