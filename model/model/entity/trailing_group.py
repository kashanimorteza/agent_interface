"""Trailing Group Entity."""

from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class TrailingGroup(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Group",
        description="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
        primary_key="id",
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
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
        ),
        unique_constraints=(("user_id", "name"),),
    )
    __tablename__ = "TrailingGroup"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    user_id: int = storage.field(declaration, "user_id")
    name: str = storage.field(declaration, "name")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
