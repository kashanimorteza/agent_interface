"""The Partial Group Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class PartialGroup(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Partial Group",
        description=(
            "Defines an independent group of rules for managing "
            "portions of an open trade. Its rules determine how "
            "much of the trade volume must be closed when profit "
            "or loss reaches specified thresholds."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description="Identifies the user who owns the partial group.",
            ),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The partial group's display name.",
            ),
            activity("Indicates whether the partial group is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the partial group.",
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
