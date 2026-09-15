"""The User Domain Definition."""

from __future__ import annotations

from model.foundation import DomainModel, FieldContract, PersistenceContract


class User(DomainModel):
    """An independent user of the system, enabling multi-user operation.

    Each user can have a separate set of settings, allowing new users to be
    added with configurations that remain distinct from those of existing
    users.
    """

    id: int | None = None
    name: str
    username: str
    password: str
    api_key: str
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "name": FieldContract(unique=True, nullable=False),
            "username": FieldContract(unique=True, nullable=False),
            "password": FieldContract(nullable=False, credential="hash"),
            "api_key": FieldContract(nullable=False, credential="hash"),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
    )
