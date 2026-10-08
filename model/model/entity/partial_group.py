"""The Partial Group Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class PartialGroup(Foundation, table=True):
    __tablename__ = "PartialGroup"
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Group",
        description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "user_id",
                FieldType.integer,
                False,
                description="Identifies the user who owns the partial group.",
            ),
            FieldDeclaration(
                "name",
                FieldType.string,
                False,
                description="The partial group's display name.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the partial group is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the partial group.",
            ),
        ),
        primary_key="id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(("user_id", "name"),),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    user_id: int = realize_field(declaration, "user_id")
    name: str = realize_field(declaration, "name")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
