"""The Broker Entity."""

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


class Broker(Entity, table=True):
    """The Broker Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Broker",
        description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The broker's display name.",
            ),
            FieldDeclaration(
                name="user_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the user who owns the broker configuration.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the broker is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the broker.",
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
    name: str
    user_id: int
    is_active: bool = True
    description: str | None = None
