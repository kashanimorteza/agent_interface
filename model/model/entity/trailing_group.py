"""The Trailing Group Entity."""

from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class TrailingGroup(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Group",
        description=(
            "Defines an independent group for organizing the rules that manage Stop Loss and "
            "Take Profit during a trade. The group identifies the rule set, while each rule "
            "separately defines its activation condition and the changes to apply."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the user who owns the trailing group.",
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The trailing group's display name.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the trailing group is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the trailing group.",
            ),
        ),
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(UniquenessConstraint(("user_id", "name")),),
    )

    __tablename__ = "TrailingGroup"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    user_id: int = mapped_field(declaration, "user_id")
    name: str = mapped_field(declaration, "name")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
