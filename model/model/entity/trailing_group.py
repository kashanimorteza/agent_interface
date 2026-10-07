"""Trailing Group Entity."""

from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Trailing Group",
    description="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the user who owns the trailing group.",
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The trailing group's display name.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the trailing group is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the trailing group.",
        ),
    ),
    primary_key="id",
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(fields=("user_id", "name")),),
)


class TrailingGroup(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    user_id: int = realize_field(DECLARATION, "user_id")
    name: str = realize_field(DECLARATION, "name")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
