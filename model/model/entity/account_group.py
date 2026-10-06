"""The Account Group Entity."""

from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Account Group",
    description=("Defines an independent group for organizing trading accounts owned by one user."),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the user who owns the account group.",
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The account group's display name.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the account group is active.",
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the account group.",
        ),
    ),
    primary_key="id",
    relations=(Relation(local_field="user_id", target_entity="User", target_field="id"),),
    unique_constraints=(UniqueConstraint(fields=("user_id", "name")),),
)


class AccountGroup(Foundation, table=True):
    """Account Group."""

    __tablename__ = "AccountGroup"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    name: str = column(_DECLARATION, "name")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
