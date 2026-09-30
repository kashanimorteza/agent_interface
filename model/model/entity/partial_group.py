"""The Partial Group Entity."""

from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class PartialGroup(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Group",
        description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
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
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the partial group is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the partial group.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            Relation("user_id", "User", "id"),
        ),
        unique_constraints=(
            ("user_id", "name"),
        ),
    )

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None
