"""The Trailing Rule Domain Definition: one rule within a Trailing Group telling the system when and how to manage Take Profit and Stop Loss."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class TrailingRule(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [
        ["trailing_group_id", "trigger_percentage"]
    ]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    name: str = domain_field(
        type="string",
        nullable=False,
        unique=True,
        description="The trailing rule's display name.",
    )
    trailing_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="TrailingGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the trailing group that contains the rule.",
    )
    trigger_percentage: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Defines the profit percentage of the take-profit target that activates the rule.",
    )
    take_profit_adjustment: Decimal | None = domain_field(
        type="decimal",
        nullable=True,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = domain_field(
        type="decimal",
        nullable=True,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the trailing rule is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the trailing rule."
    )
