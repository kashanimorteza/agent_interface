"""The Broker Entity."""

from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)


class Broker(EntityBase):
    """The Broker Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Broker",
        description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                description="The broker's display name.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns the broker configuration.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the broker is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the broker.",
                type=FieldType.STRING,
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
