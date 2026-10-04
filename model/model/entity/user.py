"""The User Entity."""

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import table_arguments
from model.core.declaration import Declaration, FieldDeclaration


class User(Entity, table=True):
    """The User Entity."""

    __tablename__ = "User"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments()

    declaration = Declaration(
        name="User",
        description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        fields=(
            identity_declaration(),
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
            activity_declaration("Indicates whether the user is active."),
            FieldDeclaration(
                name="description",
                description="Describes the user.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        unique_constraints=(("name",), ("username",)),
    )

    id: int | None = identity_field()
    name: str = Field(unique=True, description="The user's display name.")
    username: str = Field(
        unique=True, description="The username used to identify the user."
    )
    password: str = Field(description="The password credential used by the user.")
    api_key: str = Field(description="The API key assigned to the user.")
    is_active: bool = activity_field("Indicates whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")
