"""The User Entity."""

from typing import ClassVar

from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
)
from my_model.model_foundation import Model_Foundation


class User(Model_Foundation, table=True):
    """An independent user of the system, enabling multi-user operation with separate settings."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="User",
        purpose="An independent user of the system, enabling multi-user operation with separate settings.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The user's display name.",
            ),
            FieldDeclaration(
                name="username",
                type="string",
                nullable=False,
                purpose="The username used to identify the user.",
            ),
            FieldDeclaration(
                name="password",
                type="string",
                nullable=False,
                purpose="The password credential used by the user.",
                sensitive=True,
            ),
            FieldDeclaration(
                name="api_key",
                type="string",
                nullable=False,
                purpose="The API key assigned to the user.",
                sensitive=True,
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the user is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the user.",
            ),
        ),
        unique_constraints=(
            ("name",),
            ("username",),
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None
