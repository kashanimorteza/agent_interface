"""The Trailing Group Entity."""

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


class TrailingGroup(Entity, table=True):
    """The Trailing Group Entity."""

    __tablename__ = "TrailingGroup"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("user_id", "name"),
    )

    declaration = Declaration(
        name="Trailing Group",
        description="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the trailing group.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The trailing group's display name.",
                type="string",
                nullable=False,
            ),
            activity_declaration("Indicates whether the trailing group is active."),
            FieldDeclaration(
                name="description",
                description="Describes the trailing group.",
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
        description="Identifies the user who owns the trailing group.",
    )
    name: str = Field(description="The trailing group's display name.")
    is_active: bool = activity_field("Indicates whether the trailing group is active.")
    description: str | None = Field(
        default=None, description="Describes the trailing group."
    )
