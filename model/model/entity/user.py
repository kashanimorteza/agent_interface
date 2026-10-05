from typing import ClassVar

from sqlalchemy import Identity
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration


class User(EntityBase, table=True):
    __table_args__ = ({"sqlite_autoincrement": True},)
    declaration: ClassVar[Declaration] = Declaration(
        "User",
        "Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("name", "The user's display name.", "string", False),
            FieldDeclaration("username", "The username used to identify the user.", "string", False),
            FieldDeclaration("password", "The password credential used by the user.", "string", False),
            FieldDeclaration("api_key", "The API key assigned to the user.", "string", False),
            FieldDeclaration(
                "is_active", "Indicates whether the user is active.", "boolean", False, has_default=True, default=True
            ),
            FieldDeclaration("description", "Describes the user.", "string", True),
        ),
        "id",
        unique_constraints=(
            ("name",),
            ("username",),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    name: str = Field(unique=True, description="The user's display name.")
    username: str = Field(unique=True, description="The username used to identify the user.")
    password: str = Field(description="The password credential used by the user.")
    api_key: str = Field(description="The API key assigned to the user.")
    is_active: bool = Field(default=True, description="Indicates whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")
