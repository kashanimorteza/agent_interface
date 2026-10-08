"""User Entity."""

from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Sensitivity,
    ValueGeneration,
)
from model.core.foundation import Foundation


class User(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="User",
        description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
        primary_key="id",
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
                sensitivity=Sensitivity.password,
            ),
            FieldDeclaration(
                name="api_key",
                type=FieldType.string,
                nullable=False,
                description="The API key assigned to the user.",
                sensitivity=Sensitivity.sensitive,
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
        unique_constraints=(
            ("name",),
            ("username",),
        ),
    )
    __tablename__ = "User"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    name: str = storage.field(declaration, "name")
    username: str = storage.field(declaration, "username")
    password: str = storage.field(declaration, "password")
    api_key: str = storage.field(declaration, "api_key")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
