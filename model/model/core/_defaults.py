"""Universal Identity and Activity Fields, realized from the Model's Entity defaults."""

from typing import Any

from sqlalchemy import Identity
from sqlmodel import Field

from model.core.declaration import FieldDeclaration


def identity_declaration(description: str | None = None) -> FieldDeclaration:
    """Declare the Identity Field every Entity has."""
    return FieldDeclaration(
        name="id",
        description=description,
        type="integer",
        nullable=False,
        immutable=True,
        value_generation="auto_increment",
    )


def activity_declaration(description: str | None = None) -> FieldDeclaration:
    """Declare the Activity Field every Entity has."""
    return FieldDeclaration(
        name="is_active",
        description=description,
        type="boolean",
        nullable=False,
        default=True,
    )


def identity_field(description: str | None = None) -> Any:
    """Realize the Identity Field: pending until storage assigns it."""
    return Field(
        default=None,
        primary_key=True,
        description=description,
        sa_column_args=[Identity()],
    )


def activity_field(description: str | None = None) -> Any:
    """Realize the Activity Field: active unless stated otherwise."""
    return Field(default=True, description=description)
