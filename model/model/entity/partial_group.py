"""The Partial Group Entity."""

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


class PartialGroup(Entity, table=True):
    """The Partial Group Entity."""

    __tablename__ = "PartialGroup"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("user_id", "name"),
    )

    declaration = Declaration(
        name="Partial Group",
        description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the partial group.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The partial group's display name.",
                type="string",
                nullable=False,
            ),
            activity_declaration("Indicates whether the partial group is active."),
            FieldDeclaration(
                name="description",
                description="Describes the partial group.",
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
    user_id: int = Field(
        foreign_key="User.id",
        description="Identifies the user who owns the partial group.",
    )
    name: str = Field(description="The partial group's display name.")
    is_active: bool = activity_field("Indicates whether the partial group is active.")
    description: str | None = Field(
        default=None, description="Describes the partial group."
    )
