from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration, Relation


class TrailingGroup(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Trailing Group",
        "Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("user_id", "Identifies the user who owns the trailing group.", "integer", False),
            FieldDeclaration("name", "The trailing group's display name.", "string", False),
            FieldDeclaration(
                "is_active",
                "Indicates whether the trailing group is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the trailing group.", "string", True),
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
    user_id: int = Field(foreign_key="User.id", description="Identifies the user who owns the trailing group.")
    name: str = Field(description="The trailing group's display name.")
    is_active: bool = Field(default=True, description="Indicates whether the trailing group is active.")
    description: str | None = Field(default=None, description="Describes the trailing group.")
