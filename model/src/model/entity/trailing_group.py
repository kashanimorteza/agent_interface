"""The Trailing Group Entity."""

from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class TrailingGroup(Entity, table=True):
    """The Trailing Group Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Group",
        description="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the user who owns the trailing group.",
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The trailing group's display name.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the trailing group is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the trailing group.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
        ),
        unique_constraints=(UniqueConstraint(fields=("user_id", "name")),),
    )

    __table_args__ = (TableUniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None
