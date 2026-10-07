"""The Broker Entity."""

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
    name="Broker",
    description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The broker's display name.",
        ),
        FieldDeclaration(
            "user_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the user who owns the broker configuration.",
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the broker is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the broker.",
        ),
    ),
    relations=(Relation("user_id", "User", "id"),),
    unique_constraints=(UniqueConstraint(("user_id", "name")),),
)


class Broker(Foundation, table=True):
    __tablename__ = "Broker"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    user_id: int = realize_field(DECLARATION, "user_id")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
