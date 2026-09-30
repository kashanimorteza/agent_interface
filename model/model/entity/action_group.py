"""The Action Group Entity."""

from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class ActionGroup(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Action Group",
        description="Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the action group.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The action group's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the action group is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the action group.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            Relation("user_id", "User", "id"),
        ),
        unique_constraints=(
            ("user_id", "name"),
        ),
    )

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None
