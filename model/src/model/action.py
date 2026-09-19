"""Action Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
* `risk_by_reward`, `take_profit`, and `stop_loss` are exact decimal values with no declared precision, because the Target states type `decimal` and no precision.
"""

from typing import Annotated

from model.account import Account
from model.action_group import ActionGroup
from model.asset import Asset
from model.foundation import (
    ActiveFlag,
    ExactDecimal,
    GeneratedIdentity,
    ModelFoundation,
)
from model.partial_group import PartialGroup
from model.trailing_group import TrailingGroup
from model.vocabulary import Cardinality, Persistence, Reference


class Action(ModelFoundation):
    """How a position must be opened: the asset and account, and the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("action_group_id", "name"),)

    id: GeneratedIdentity = None
    name: str
    action_group_id: Annotated[
        int,
        Reference(
            definition=ActionGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    asset_id: Annotated[
        int,
        Reference(
            definition=Asset, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    account_id: Annotated[
        int,
        Reference(
            definition=Account, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    partial_group_id: Annotated[
        int,
        Reference(
            definition=PartialGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    trailing_group_id: Annotated[
        int,
        Reference(
            definition=TrailingGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    risk_by_reward: ExactDecimal
    take_profit: ExactDecimal
    stop_loss: ExactDecimal
    is_active: ActiveFlag = True
    description: str | None = None
