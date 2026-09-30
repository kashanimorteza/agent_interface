"""The Trailing Group Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class TrailingGroup(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Trailing Group",
        description=(
            "Defines an independent group for organizing the "
            "rules that manage Stop Loss and Take Profit during a "
            "trade. The group identifies the rule set, while each "
            "rule separately defines its activation condition and "
            "the changes to apply."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description="Identifies the user who owns the trailing group.",
            ),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The trailing group's display name.",
            ),
            activity("Indicates whether the trailing group is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the trailing group.",
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
