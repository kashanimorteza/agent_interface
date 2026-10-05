from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration, Relation


class PartialGroup(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Partial Group",
        "Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("user_id", "Identifies the user who owns the partial group.", "integer", False),
            FieldDeclaration("name", "The partial group's display name.", "string", False),
            FieldDeclaration(
                "is_active",
                "Indicates whether the partial group is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the partial group.", "string", True),
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
    user_id: int = Field(foreign_key="User.id", description="Identifies the user who owns the partial group.")
    name: str = Field(description="The partial group's display name.")
    is_active: bool = Field(default=True, description="Indicates whether the partial group is active.")
    description: str | None = Field(default=None, description="Describes the partial group.")
