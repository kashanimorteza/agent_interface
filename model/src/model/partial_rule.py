"""The Partial Rule Domain Definition: one Partial Close rule telling the system when and how much of an open position must be closed."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class PartialRule(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["partial_group_id", "profit_percentage"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    name: str = domain_field(
        type="string",
        nullable=False,
        unique=True,
        description="The partial rule's display name.",
    )
    partial_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="PartialGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the partial group that contains the rule.",
    )
    profit_percentage: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Defines the profit percentage that activates the rule.",
    )
    close_percentage: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Defines the percentage of the position closed when the rule is activated.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the partial rule is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the partial rule."
    )
