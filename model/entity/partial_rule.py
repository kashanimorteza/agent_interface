from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class PartialRule(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Rule",
        description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
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
                description="The partial rule's display name.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the partial group that contains the rule.",
            ),
            FieldDeclaration(
                name="profit_percentage",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the profit percentage that activates the rule.",
            ),
            FieldDeclaration(
                name="close_percentage",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the percentage of the position closed when the rule is activated.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the partial rule is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the partial rule.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(
                local_field="partial_group_id", target_entity="Partial Group", target_field="id"
            ),
        ),
        unique_constraints=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    partial_group_id: int
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
