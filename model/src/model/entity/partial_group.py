"""The Partial Group Entity."""

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


class PartialGroup(Entity, table=True):
    """The Partial Group Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Group",
        description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
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
                description="Identifies the user who owns the partial group.",
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The partial group's display name.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the partial group is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the partial group.",
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
