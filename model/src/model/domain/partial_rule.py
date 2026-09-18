"""The Partial Rule Domain Definition: one condition and close percentage within a Partial Group."""

from decimal import Decimal
from typing import ClassVar

from model.foundation import DomainModel, domain_field


class PartialRule(DomainModel):
    """A rule telling the system under which condition, and how much of, an open position must be closed."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("partial_group_id", "profit_percentage"),
    )

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the partial rule.",
    )
    name: str = domain_field(
        unique=True, description="The partial rule's display name."
    )
    partial_group_id: int = domain_field(
        foreign_key="PartialGroup.id",
        cardinality="many_to_one",
        description="Identifies the partial group that contains the rule.",
    )
    profit_percentage: Decimal = domain_field(
        description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = domain_field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the partial rule is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the partial rule."
    )
