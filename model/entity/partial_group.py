from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class PartialGroup(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Group",
        description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
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
                name="user_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the user who owns the partial group.",
            ),
            FieldDeclaration(
                name="name",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The partial group's display name.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the partial group is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the partial group.",
            ),
        ),
        primary_key="id",
        relations=(Relation(local_field="user_id", target_entity="User", target_field="id"),),
        unique_constraints=(("user_id", "name"),),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None
