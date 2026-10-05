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
    name="Broker",
    description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
    fields=(
        identity(),
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
        activity("Indicates whether the broker is active."),
        FieldDeclaration(
            name="description",
            description="Describes the broker.",
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


class Broker(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    user_id: int = column(_DECLARATION, "user_id")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
