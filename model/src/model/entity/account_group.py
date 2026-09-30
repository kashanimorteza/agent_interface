"""The Account Group Entity."""

from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)


class AccountGroup(EntityBase):
    """The Account Group Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Account Group",
        description="Defines an independent group for organizing trading accounts owned by one user.",
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
                name="user_id",
                description="Identifies the user who owns the account group.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="name",
                description="The account group's display name.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the account group is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the account group.",
                type=FieldType.STRING,
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(("user_id", "name"),),
    )

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None
