"""The Action Group Domain Definition: an independent grouping for trading actions based on their risk profile."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class ActionGroup(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["user_id", "name"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    user_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="User", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the user who owns the action group.",
    )
    name: str = domain_field(
        type="string", nullable=False, description="The action group's display name."
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the action group is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the action group."
    )
