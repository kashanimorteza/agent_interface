"""The Broker Domain Definition: a broker supported by the system, owned by a user, independent of any one Trading Platform."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class Broker(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["user_id", "name"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    name: str = domain_field(
        type="string", nullable=False, description="The broker's display name."
    )
    user_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="User", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the user who owns the broker configuration.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the broker is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the broker."
    )
