"""The Broker Entity."""

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class Broker(Entity, table=True):
    """The Broker Entity."""

    __tablename__ = "Broker"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("user_id", "name"),
    )

    declaration = Declaration(
        name="Broker",
        description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="name",
                description="The broker's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the broker configuration.",
                type="integer",
                nullable=False,
            ),
            activity_declaration("Indicates whether the broker is active."),
            FieldDeclaration(
                name="description",
                description="Describes the broker.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="user_id", target_entity="User", target_field="id"
            ),
        ),
        unique_constraints=(("user_id", "name"),),
    )

    id: int | None = identity_field()
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(
        foreign_key="User.id",
        description="Identifies the user who owns the broker configuration.",
    )
    is_active: bool = activity_field("Indicates whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")
