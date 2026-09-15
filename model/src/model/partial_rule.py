"""The Partial Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class PartialRule(DomainModel):
    """An individual Partial Close rule.

    Tells the system under which condition part of an open position must be
    closed and how much of its volume must be closed.
    """

    id: int | None = None
    name: str
    partial_group_id: int
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "name": FieldContract(unique=True, nullable=False),
            "partial_group_id": FieldContract(nullable=False),
            "profit_percentage": FieldContract(nullable=False),
            "close_percentage": FieldContract(nullable=False),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(
            RelationshipContract(field="partial_group_id", references="PartialGroup"),
        ),
        unique_sets=(("partial_group_id", "profit_percentage"),),
    )
