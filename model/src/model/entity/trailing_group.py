"""The Trailing Group Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Trailing Group",
    description="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
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
            description="Identifies the user who owns the trailing group.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="name",
            description="The trailing group's display name.",
            type="string",
            nullable=False,
        ),
        FieldDeclaration(
            name="is_active",
            description="Indicates whether the trailing group is active.",
            type="boolean",
            nullable=False,
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            description="Describes the trailing group.",
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


class TrailingGroup(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    user_id: int = Field(
        description="Identifies the user who owns the trailing group.",
        **column_options(_DECLARATION, "user_id"),
    )
    name: str = Field(
        description="The trailing group's display name.",
        **column_options(_DECLARATION, "name"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the trailing group is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the trailing group.",
        **column_options(_DECLARATION, "description"),
    )
