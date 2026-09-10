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
from my_model._models.partial_group import PartialGroup


class PartialRule(DomainModel):
    """A Partial Close rule stating when part of an open position is closed and how much of its volume."""

    logical_name = "Partial Rule"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The partial rule's display name.")
    partial_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = field(
        LogicalType.DECIMAL, nullable=False, purpose="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = field(
        LogicalType.DECIMAL,
        nullable=False,
        purpose="Defines the percentage of the position closed when the rule is activated.",
    )
    status: bool = field(
        LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the partial rule is active."
    )
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the partial rule.")

    declared_relationships = (
        Relationship(
            role="partial group",
            target=PartialGroup,
            field="partial_group_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one Partial Group through `partial_group_id`.",
        ),
    )
