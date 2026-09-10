from decimal import Decimal

from my_model._declarations import (
    AwaitingGeneration,
    Cardinality,
    DomainModel,
    LogicalType,
    Participation,
    Relationship,
    RelationshipKind,
    field,
)
from my_model._models.trailing_group import TrailingGroup


class TrailingRule(DomainModel):
    """A rule within a Trailing Group stating when and how Take Profit and Stop Loss are adjusted."""

    logical_name = "Trailing Rule"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The trailing rule's display name.")
    trailing_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = field(
        LogicalType.DECIMAL,
        nullable=False,
        purpose="Defines the profit percentage of the take-profit target that activates the rule.",
    )
    take_profit_adjustment: Decimal | None = field(
        LogicalType.DECIMAL,
        nullable=True,
        purpose="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = field(
        LogicalType.DECIMAL,
        nullable=True,
        purpose="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    status: bool = field(
        LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the trailing rule is active."
    )
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the trailing rule.")

    declared_relationships = (
        Relationship(
            role="trailing group",
            target=TrailingGroup,
            field="trailing_group_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one Trailing Group through `trailing_group_id`.",
        ),
    )
