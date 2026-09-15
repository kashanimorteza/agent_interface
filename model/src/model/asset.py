"""The Asset Domain Definition."""

from __future__ import annotations

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class Asset(DomainModel):
    """An asset that can be selected for trading.

    Provides the system with the complete set of available tradable assets
    and identifies the category of each asset so the system knows exactly
    what is being traded.
    """

    id: int | None = None
    broker_id: int
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "broker_id": FieldContract(nullable=False),
            "symbol": FieldContract(nullable=False),
            "category": FieldContract(nullable=False),
            "point_size": FieldContract(nullable=False, default=0.0),
            "digits": FieldContract(nullable=False, default=0),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(RelationshipContract(field="broker_id", references="Broker"),),
        unique_sets=(("broker_id", "symbol"),),
    )
