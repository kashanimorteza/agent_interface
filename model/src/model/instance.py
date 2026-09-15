"""The Instance Domain Definition."""

from __future__ import annotations

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class Instance(DomainModel):
    """A user-owned connection instance through which the system accesses a
    supported Trading Platform.

    The Trading Platform selected through ``trading_platform_id`` defines
    which of the technical connection fields are required; every field it
    requires must be present before the Instance can be used. That
    cross-Domain-Definition rule is not evaluable from Instance data alone
    and is enforced outside Model.
    """

    id: int | None = None
    user_id: int
    trading_platform_id: int
    name: str
    ip: str | None = None
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "user_id": FieldContract(nullable=False),
            "trading_platform_id": FieldContract(nullable=False),
            "name": FieldContract(nullable=False),
            "ip": FieldContract(nullable=True),
            "username": FieldContract(nullable=True),
            "password": FieldContract(nullable=True, credential="encrypted"),
            "api_key": FieldContract(nullable=True, credential="encrypted"),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(
            RelationshipContract(field="user_id", references="User"),
            RelationshipContract(
                field="trading_platform_id", references="TradingPlatform"
            ),
        ),
        unique_sets=(("user_id", "name"),),
    )
