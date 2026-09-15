"""The Action Group Domain Definition."""

from __future__ import annotations

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class ActionGroup(DomainModel):
    """An independent grouping for trading actions based on their risk
    profile, such as high risk, normal risk, or low risk.

    Actions are assigned to these groups so trades can be organized and
    selected by their intended risk level.
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
