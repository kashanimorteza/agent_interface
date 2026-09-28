"""Partial Rule Entity."""

from decimal import Decimal

from model.declaration import Declaration
from model.entity.partial_group import PartialGroup
from model.foundation import Foundation


class PartialRule(Foundation, table=True):
    """Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed."""

    id: int | None = Declaration.identity()
    name: str = Declaration.field(
        unique=True, description="The partial rule's display name."
    )
    partial_group_id: int = Declaration.field(
        reference=PartialGroup,
        description="Identifies the partial group that contains the rule.",
    )
    profit_percentage: Decimal = Declaration.field(
        description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = Declaration.field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the partial rule is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the partial rule."
    )

    __table_args__ = Declaration.composite(
        "PartialRule", unique=(("partial_group_id", "profit_percentage"),)
    )
