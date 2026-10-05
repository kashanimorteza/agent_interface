from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Trailing Group",
    description="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
    fields=(
        identity(),
        FieldDeclaration(
            name="user_id",
            description="Identifies the user who owns the trailing group.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="name",
            description="The trailing group's display name.",
            type=FieldType.STRING,
            nullable=False,
        ),
        activity("Indicates whether the trailing group is active."),
        FieldDeclaration(
            name="description",
            description="Describes the trailing group.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(RelationDeclaration("user_id", "User", "id"),),
    unique_constraints=(
        UniqueConstraintDeclaration(
            (
                "user_id",
                "name",
            )
        ),
    ),
)


class TrailingGroup(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    name: str = column(_DECLARATION, "name")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
