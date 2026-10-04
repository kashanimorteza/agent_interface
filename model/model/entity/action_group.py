"""The Action Group Entity."""

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


class ActionGroup(Entity, table=True):
    """The Action Group Entity."""

    __tablename__ = "ActionGroup"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("user_id", "name"),
    )

    declaration = Declaration(
        name="Action Group",
        description="Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.",
        fields=(
            identity_declaration(),
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
            activity_declaration("Indicates whether the action group is active."),
            FieldDeclaration(
                name="description",
                description="Describes the action group.",
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
        description="Identifies the user who owns the action group.",
    )
    name: str = Field(description="The action group's display name.")
    is_active: bool = activity_field("Indicates whether the action group is active.")
    description: str | None = Field(
        default=None, description="Describes the action group."
    )
