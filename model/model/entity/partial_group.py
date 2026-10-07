"""The Partial Group Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Partial Group",
    description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "user_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the user who owns the partial group.",
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The partial group's display name.",
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the partial group is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the partial group.",
        ),
    ),
    relations=(Relation("user_id", "User", "id"),),
    unique_constraints=(UniqueConstraint(("user_id", "name")),),
)


class PartialGroup(Foundation, table=True):
    __tablename__ = "PartialGroup"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    user_id: int = realize_field(DECLARATION, "user_id")
    name: str = realize_field(DECLARATION, "name")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
