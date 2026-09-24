"""The Action Domain Definition."""

from typing import Annotated

from model.entity.account import Account
from model.entity.action_group import ActionGroup
from model.entity.asset import Asset
from model.entity.partial_group import PartialGroup
from model.entity.trailing_group import TrailingGroup
from model.foundation import (
    Constraint,
    Declare,
    ExactDecimal,
    ModelFoundation,
    Relationship,
)

__all__ = ["Action"]


class Action(
    ModelFoundation,
    description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="action_group",
            description="Belongs to one Action Group through `action_group_id`.",
            definition=ActionGroup,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="asset",
            description="Uses one Asset through `asset_id`.",
            definition=Asset,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="account",
            description="Uses one Account through `account_id`.",
            definition=Account,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="partial_group",
            description="Uses one Partial Group through `partial_group_id`.",
            definition=PartialGroup,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="trailing_group",
            description="Uses one Trailing Group through `trailing_group_id`.",
            definition=TrailingGroup,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="action_action_group_id_name_unique",
            description="The combination of `action_group_id` and `name` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the action.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    name: Annotated[
        str, Declare(description="The action's display name.", logical_type="string")
    ]
    action_group_id: Annotated[
        int,
        Declare(
            description="Identifies the action group that contains the action.",
            logical_type="integer",
        ),
    ]
    asset_id: Annotated[
        int,
        Declare(
            description="Identifies the asset traded by the action.",
            logical_type="integer",
        ),
    ]
    account_id: Annotated[
        int,
        Declare(
            description="Identifies the account used to execute the action.",
            logical_type="integer",
        ),
    ]
    partial_group_id: Annotated[
        int,
        Declare(
            description="Identifies the Partial Group used by the action.",
            logical_type="integer",
        ),
    ]
    trailing_group_id: Annotated[
        int,
        Declare(
            description="Identifies the Trailing Group used by the action.",
            logical_type="integer",
        ),
    ]
    risk_by_reward: Annotated[
        ExactDecimal,
        Declare(
            description="Defines the numeric risk-to-reward value used by the action.",
            logical_type="decimal",
        ),
    ]
    take_profit: Annotated[
        ExactDecimal,
        Declare(
            description="Defines the Take Profit value used by the action.",
            logical_type="decimal",
        ),
    ]
    stop_loss: Annotated[
        ExactDecimal,
        Declare(
            description="Defines the Stop Loss value used by the action.",
            logical_type="decimal",
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the action is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None, Declare(description="Describes the action.", logical_type="string")
    ]
