"""Partial Rule: one Partial Close rule within a Partial Group."""

from __future__ import annotations

from decimal import Decimal

from .base import Model, Relationship, field
from .partial_group import PartialGroup


class PartialRule(Model):
    """Defines an individual Partial Close rule that tells the system under
    which condition part of an open position must be closed and how much of
    its volume must be closed."""

    logical_name = "Partial Rule"

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The partial rule's display name.")
    partial_group_id: int = field(
        "integer", purpose="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = field(
        "decimal", purpose="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = field(
        "decimal",
        purpose="Defines the percentage of the position closed when the rule is activated.",
    )
    status: bool = field("boolean", default=True, purpose="Indicates whether the partial rule is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the partial rule.")

    relationships = (
        Relationship(field="partial_group_id", target=PartialGroup, kind="belongs_to"),
    )
