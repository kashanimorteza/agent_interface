"""The Trailing Group Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class TrailingGroup(Model_Foundation, table=True):
    """An independent group of rules that manage Stop Loss and Take Profit during a trade."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="TrailingGroup",
        purpose="An independent group of rules that manage Stop Loss and Take Profit during a trade.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="user_id",
                type="integer",
                nullable=False,
                purpose="Identifies the user who owns the trailing group.",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The trailing group's display name.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the trailing group is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the trailing group.",
            ),
        ),
        references=(ReferenceDeclaration(field="user_id", entity="User"),),
        unique_constraints=(("user_id", "name"),),
    )
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    is_active: bool = True
    description: str | None = None
