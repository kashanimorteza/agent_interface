"""The Partial Group Domain Definition."""

from __future__ import annotations

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class PartialGroup(DomainModel):
    """An independent group of rules for managing portions of an open trade.

    Its rules determine how much of the trade volume must be closed when
    profit or loss reaches specified thresholds.
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
