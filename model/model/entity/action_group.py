"""The Action Group Entity."""

from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Action Group",
    description=(
        "Defines an independent grouping for trading actions based on their "
        "risk profile, such as high risk, normal risk, or low risk. Actions "
        "are assigned to these groups so trades can be organized and selected "
        "by their intended risk level."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the user who owns the action group.",
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The action group's display name.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the action group is active.",
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the action group.",
        ),
    ),
    primary_key="id",
    relations=(Relation(local_field="user_id", target_entity="User", target_field="id"),),
    unique_constraints=(UniqueConstraint(fields=("user_id", "name")),),
)


class ActionGroup(Foundation, table=True):
    """Action Group."""

    __tablename__ = "ActionGroup"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    name: str = column(_DECLARATION, "name")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
