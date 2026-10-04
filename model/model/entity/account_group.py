"""The Account Group Entity."""

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


class AccountGroup(Entity, table=True):
    """The Account Group Entity."""

    __tablename__ = "AccountGroup"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("user_id", "name"),
    )

    declaration = Declaration(
        name="Account Group",
        description="Defines an independent group for organizing trading accounts owned by one user.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the account group.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The account group's display name.",
                type="string",
                nullable=False,
            ),
            activity_declaration("Indicates whether the account group is active."),
            FieldDeclaration(
                name="description",
                description="Describes the account group.",
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
        description="Identifies the user who owns the account group.",
    )
    name: str = Field(description="The account group's display name.")
    is_active: bool = activity_field("Indicates whether the account group is active.")
    description: str | None = Field(
        default=None, description="Describes the account group."
    )
