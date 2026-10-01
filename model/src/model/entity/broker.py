"""The Broker Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Broker",
    description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
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
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(("user_id", "name"),),
    indexes=(),
)


class Broker(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    name: str = Field(
        description="The broker's display name.", **column_options(_DECLARATION, "name")
    )
    user_id: int = Field(
        description="Identifies the user who owns the broker configuration.",
        **column_options(_DECLARATION, "user_id"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the broker is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the broker.",
        **column_options(_DECLARATION, "description"),
    )
