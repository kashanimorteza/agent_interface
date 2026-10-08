"""Broker Entity."""

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


class Broker(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Broker",
        description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
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
                name="name",
                type=FieldType.string,
                nullable=False,
                description="The broker's display name.",
            ),
            FieldDeclaration(
                name="user_id",
                type=FieldType.integer,
                nullable=False,
                description="Identifies the user who owns the broker configuration.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.boolean,
                nullable=False,
                description="Indicates whether the broker is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.string,
                nullable=True,
                description="Describes the broker.",
            ),
        ),
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
        ),
        unique_constraints=(("user_id", "name"),),
    )
    __tablename__ = "Broker"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    name: str = storage.field(declaration, "name")
    user_id: int = storage.field(declaration, "user_id")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
