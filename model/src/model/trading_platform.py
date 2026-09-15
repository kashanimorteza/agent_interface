"""The Trading Platform Domain Definition."""

from __future__ import annotations

from model.foundation import DomainModel, FieldContract, PersistenceContract


class TradingPlatform(DomainModel):
    """A supported trading API standard, such as MetaTrader 5 or Binance.

    Every trading platform implementation exposes the same
    application-facing trading functions through a dedicated class, while
    handling communication with its destination API according to that
    platform's own mechanism. Additional platform implementations can be
    added without changing the system's common trading interface.
    """

    id: int | None = None
    name: str
    code: str
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "name": FieldContract(unique=True, nullable=False),
            "code": FieldContract(nullable=False),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
    )
