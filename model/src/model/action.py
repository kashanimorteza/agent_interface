"""The Action Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class Action(DomainModel):
    """How a position must be opened.

    An action selects the asset and account and provides the risk, Take
    Profit, Stop Loss, Partial Group, and Trailing Group settings that
    determine the position's parameters and execution behavior.
    """

    id: int | None = None
    name: str
    action_group_id: int
    asset_id: int
    account_id: int
    partial_group_id: int
    trailing_group_id: int
    risk_by_reward: Decimal
    take_profit: Decimal
    stop_loss: Decimal
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "name": FieldContract(nullable=False),
            "action_group_id": FieldContract(nullable=False),
            "asset_id": FieldContract(nullable=False),
            "account_id": FieldContract(nullable=False),
            "partial_group_id": FieldContract(nullable=False),
            "trailing_group_id": FieldContract(nullable=False),
            "risk_by_reward": FieldContract(nullable=False),
            "take_profit": FieldContract(nullable=False),
            "stop_loss": FieldContract(nullable=False),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(
            RelationshipContract(field="action_group_id", references="ActionGroup"),
            RelationshipContract(field="asset_id", references="Asset"),
            RelationshipContract(field="account_id", references="Account"),
            RelationshipContract(field="partial_group_id", references="PartialGroup"),
            RelationshipContract(field="trailing_group_id", references="TrailingGroup"),
        ),
        unique_sets=(("action_group_id", "name"),),
    )
