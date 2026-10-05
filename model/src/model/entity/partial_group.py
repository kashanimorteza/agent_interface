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
    name="Partial Group",
    description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
    fields=(
        identity(),
        FieldDeclaration(
            name="user_id",
            description="Identifies the user who owns the partial group.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="name",
            description="The partial group's display name.",
            type=FieldType.STRING,
            nullable=False,
        ),
        activity("Indicates whether the partial group is active."),
        FieldDeclaration(
            name="description",
            description="Describes the partial group.",
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


class PartialGroup(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    name: str = column(_DECLARATION, "name")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
