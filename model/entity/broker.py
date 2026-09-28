from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class Broker(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Broker",
        description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The broker's display name.",
            ),
            FieldDeclaration(
                name="user_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the user who owns the broker configuration.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the broker is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the broker.",
            ),
        ),
        primary_key="id",
        relations=(Relation(local_field="user_id", target_entity="User", target_field="id"),),
        unique_constraints=(("user_id", "name"),),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    user_id: int
    is_active: bool = True
    description: str | None = None
