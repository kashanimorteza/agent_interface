"""The Account Group Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Account Group",
    description="Defines an independent group for organizing trading accounts owned by one user.",
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
            name="user_id",
            description="Identifies the user who owns the account group.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="name",
            description="The account group's display name.",
            type="string",
            nullable=False,
        ),
        FieldDeclaration(
            name="is_active",
            description="Indicates whether the account group is active.",
            type="boolean",
            nullable=False,
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            description="Describes the account group.",
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


class AccountGroup(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    user_id: int = Field(
        description="Identifies the user who owns the account group.",
        **column_options(_DECLARATION, "user_id"),
    )
    name: str = Field(
        description="The account group's display name.",
        **column_options(_DECLARATION, "name"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the account group is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the account group.",
        **column_options(_DECLARATION, "description"),
    )
