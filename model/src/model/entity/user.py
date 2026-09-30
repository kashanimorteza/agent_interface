"""The User Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration


class User(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="User",
        description=(
            "Defines an independent user of the system and "
            "enables multi-user operation. Each user can have a "
            "separate set of settings, allowing new users to be "
            "added with configurations that remain distinct from "
            "those of existing users."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "name", "string", nullable=False, description="The user's display name."
            ),
            FieldDeclaration(
                "username",
                "string",
                nullable=False,
                description="The username used to identify the user.",
            ),
            FieldDeclaration(
                "password",
                "string",
                nullable=False,
                description="The password credential used by the user.",
                sensitivity="password",
            ),
            FieldDeclaration(
                "api_key",
                "string",
                nullable=False,
                description="The API key assigned to the user.",
                sensitivity="sensitive",
            ),
            activity("Indicates whether the user is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the user.",
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
