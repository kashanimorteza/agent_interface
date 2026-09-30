"""The Action Group Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class ActionGroup(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Action Group",
        description=(
            "Defines an independent grouping for trading actions "
            "based on their risk profile, such as high risk, "
            "normal risk, or low risk. Actions are assigned to "
            "these groups so trades can be organized and selected "
            "by their intended risk level."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description="Identifies the user who owns the action group.",
            ),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The action group's display name.",
            ),
            activity("Indicates whether the action group is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the action group.",
            ),
        ),
        primary_key="id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(("user_id", "name"),),
    )

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None
