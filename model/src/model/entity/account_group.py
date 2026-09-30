"""The Account Group Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class AccountGroup(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Account Group",
        description=(
            "Defines an independent group for organizing trading "
            "accounts owned by one user."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description="Identifies the user who owns the account group.",
            ),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The account group's display name.",
            ),
            activity("Indicates whether the account group is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the account group.",
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
