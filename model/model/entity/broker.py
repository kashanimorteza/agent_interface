from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration, Relation


class Broker(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Broker",
        "Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("name", "The broker's display name.", "string", False),
            FieldDeclaration("user_id", "Identifies the user who owns the broker configuration.", "integer", False),
            FieldDeclaration(
                "is_active", "Indicates whether the broker is active.", "boolean", False, has_default=True, default=True
            ),
            FieldDeclaration("description", "Describes the broker.", "string", True),
        ),
        "id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(
            (
                "user_id",
                "name",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(foreign_key="User.id", description="Identifies the user who owns the broker configuration.")
    is_active: bool = Field(default=True, description="Indicates whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")
