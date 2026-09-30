"""The Broker Entity."""

from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class Broker(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Broker",
        description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                description="The broker's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the broker configuration.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the broker is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the broker.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(("user_id", "name"),),
    )

    id: int | None = None
    name: str
    user_id: int
    is_active: bool = True
    description: str | None = None
