"""The Action Domain Definition: how a position must be opened, selecting the asset and account and the position's parameters and execution behavior."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class Action(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["action_group_id", "name"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    name: str = domain_field(
        type="string", nullable=False, description="The action's display name."
    )
    action_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="ActionGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the action group that contains the action.",
    )
    asset_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Asset", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the asset traded by the action.",
    )
    account_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Account", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the account used to execute the action.",
    )
    partial_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="PartialGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the Partial Group used by the action.",
    )
    trailing_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="TrailingGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the Trailing Group used by the action.",
    )
    risk_by_reward: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Defines the numeric risk-to-reward value used by the action.",
    )
    take_profit: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Defines the Take Profit value used by the action.",
    )
    stop_loss: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Defines the Stop Loss value used by the action.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the action is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the action."
    )
