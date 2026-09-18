"""The Action Domain Definition: how a position must be opened."""

from decimal import Decimal
from typing import ClassVar

from model.foundation import DomainModel, domain_field


class Action(DomainModel):
    """Selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group,
    and Trailing Group settings that determine a position's parameters and execution behavior.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("action_group_id", "name"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the action.",
    )
    name: str = domain_field(description="The action's display name.")
    action_group_id: int = domain_field(
        foreign_key="ActionGroup.id",
        cardinality="many_to_one",
        description="Identifies the action group that contains the action.",
    )
    asset_id: int = domain_field(
        foreign_key="Asset.id",
        cardinality="many_to_one",
        description="Identifies the asset traded by the action.",
    )
    account_id: int = domain_field(
        foreign_key="Account.id",
        cardinality="many_to_one",
        description="Identifies the account used to execute the action.",
    )
    partial_group_id: int = domain_field(
        foreign_key="PartialGroup.id",
        cardinality="many_to_one",
        description="Identifies the Partial Group used by the action.",
    )
    trailing_group_id: int = domain_field(
        foreign_key="TrailingGroup.id",
        cardinality="many_to_one",
        description="Identifies the Trailing Group used by the action.",
    )
    risk_by_reward: Decimal = domain_field(
        description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = domain_field(
        description="Defines the Take Profit value used by the action."
    )
    stop_loss: Decimal = domain_field(
        description="Defines the Stop Loss value used by the action."
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the action is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the action."
    )
