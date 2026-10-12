"""The User Entity."""

from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class User(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="User",
        description=(
            "Defines an independent user of the system and enables multi-user operation. "
            "Each user can have a separate set of settings, allowing new users to be added "
            "with configurations that remain distinct from those of existing users."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The user's display name.",
            ),
            FieldDeclaration(
                name="username",
                type=FieldType.STRING,
                nullable=False,
                description="The username used to identify the user.",
            ),
            FieldDeclaration(
                name="password",
                type=FieldType.STRING,
                nullable=False,
                description="The password credential used by the user.",
                sensitivity=Sensitivity.PASSWORD,
            ),
            FieldDeclaration(
                name="api_key",
                type=FieldType.STRING,
                nullable=False,
                description="The API key assigned to the user.",
                sensitivity=Sensitivity.SENSITIVE,
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the user is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the user.",
            ),
        ),
        unique_constraints=(
            UniquenessConstraint(("name",)),
            UniquenessConstraint(("username",)),
        ),
    )

    __tablename__ = "User"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    name: str = mapped_field(declaration, "name")
    username: str = mapped_field(declaration, "username")
    password: str = mapped_field(declaration, "password")
    api_key: str = mapped_field(declaration, "api_key")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
