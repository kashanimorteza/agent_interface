"""The Trailing Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class TrailingRule(DomainModel):
    """An individual rule within a Trailing Group that tells the system when
    and how to manage Take Profit and Stop Loss.

    Each rule provides the activation condition and the parameters used to
    apply the required adjustments.
    """

    id: int | None = None
    name: str
    trailing_group_id: int
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "name": FieldContract(unique=True, nullable=False),
            "trailing_group_id": FieldContract(nullable=False),
            "trigger_percentage": FieldContract(nullable=False),
            "take_profit_adjustment": FieldContract(nullable=True),
            "stop_loss_adjustment": FieldContract(nullable=True),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(
            RelationshipContract(field="trailing_group_id", references="TrailingGroup"),
        ),
        unique_sets=(("trailing_group_id", "trigger_percentage"),),
    )
