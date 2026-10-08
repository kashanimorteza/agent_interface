"""Account Group Entity."""

from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class AccountGroup(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Account Group",
        description="Defines an independent group for organizing trading accounts owned by one user.",
        primary_key="id",
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
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.string,
                nullable=True,
                description="Describes the account group.",
            ),
        ),
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
        ),
        unique_constraints=(("user_id", "name"),),
    )
    __tablename__ = "AccountGroup"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    user_id: int = storage.field(declaration, "user_id")
    name: str = storage.field(declaration, "name")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
