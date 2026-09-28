from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class TrailingRule(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Rule",
        description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
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
                description="The trailing rule's display name.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the trailing group that contains the rule.",
            ),
            FieldDeclaration(
                name="trigger_percentage",
                type=LogicalType.DECIMAL,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the profit percentage of the take-profit target that activates the rule.",
            ),
            FieldDeclaration(
                name="take_profit_adjustment",
                type=LogicalType.DECIMAL,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the take-profit adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                name="stop_loss_adjustment",
                type=LogicalType.DECIMAL,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Defines the stop-loss adjustment applied when the rule is activated.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the trailing rule is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the trailing rule.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(
                local_field="trailing_group_id", target_entity="Trailing Group", target_field="id"
            ),
        ),
        unique_constraints=(
            ("name",),
            ("trailing_group_id", "trigger_percentage"),
        ),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    trailing_group_id: int
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None
