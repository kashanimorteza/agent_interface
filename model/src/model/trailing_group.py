"""The Trailing Group Domain Definition."""

from __future__ import annotations

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class TrailingGroup(DomainModel):
    """An independent group for organizing the rules that manage Stop Loss
    and Take Profit during a trade.

    The group identifies the rule set, while each rule separately defines
    its activation condition and the changes to apply.
    """

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "user_id": FieldContract(nullable=False),
            "name": FieldContract(nullable=False),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(RelationshipContract(field="user_id", references="User"),),
        unique_sets=(("user_id", "name"),),
    )
