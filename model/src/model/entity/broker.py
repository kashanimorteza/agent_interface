"""The Broker Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class Broker(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Broker",
        description=(
            "Defines a broker supported by the system and "
            "identifies the user who owns its configuration "
            "without coupling the Broker definition to one "
            "Trading Platform."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The broker's display name.",
            ),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description=("Identifies the user who owns the broker configuration."),
            ),
            activity("Indicates whether the broker is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the broker.",
            ),
        ),
        primary_key="id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(("user_id", "name"),),
    )

    id: int | None = None
    name: str
    user_id: int
    is_active: bool = True
    description: str | None = None
