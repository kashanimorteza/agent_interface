from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration, Relation


class ActionGroup(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Action Group",
        "Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("user_id", "Identifies the user who owns the action group.", "integer", False),
            FieldDeclaration("name", "The action group's display name.", "string", False),
            FieldDeclaration(
                "is_active",
                "Indicates whether the action group is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the action group.", "string", True),
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
    user_id: int = Field(foreign_key="User.id", description="Identifies the user who owns the action group.")
    name: str = Field(description="The action group's display name.")
    is_active: bool = Field(default=True, description="Indicates whether the action group is active.")
    description: str | None = Field(default=None, description="Describes the action group.")
