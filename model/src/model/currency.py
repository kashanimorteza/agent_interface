"""The Currency Domain Definition."""

from __future__ import annotations

from pydantic import Field

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class Currency(DomainModel):
    """A currency that can be used by the trading system.

    Identifies its standard code, display symbol, associated country or
    region, and monetary decimal precision.
    """

    id: int | None = None
    user_id: int
    code: str = Field(min_length=3, max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "user_id": FieldContract(nullable=False),
            "code": FieldContract(nullable=False),
            "symbol": FieldContract(nullable=True),
            "country": FieldContract(nullable=True),
            "decimal_digits": FieldContract(nullable=False, default=2),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(RelationshipContract(field="user_id", references="User"),),
        unique_sets=(("user_id", "code"),),
    )
