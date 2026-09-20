"""The Action Domain Definition.

How a position must be opened: its asset, account, risk, targets, and rule groups.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly. Monetary and rate values are exact decimals.
"""

from typing import Annotated

from model.account import Account
from model.action_group import ActionGroup
from model.asset import Asset
from model.declaration import (
    Activation,
    Cardinality,
    Generated,
    Identity,
    Persistence,
    Relationship,
)
from model.foundation import ExactDecimal, ModelFoundation
from model.partial_group import PartialGroup
from model.trailing_group import TrailingGroup


class Action(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="action_group",
            via="action_group_id",
            reference=ActionGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="asset",
            via="asset_id",
            reference=Asset,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="account",
            via="account_id",
            reference=Account,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="partial_group",
            via="partial_group_id",
            reference=PartialGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="trailing_group",
            via="trailing_group_id",
            reference=TrailingGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )
    unique_sets = (("action_group_id", "name"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    name: str
    action_group_id: int
    asset_id: int
    account_id: int
    partial_group_id: int
    trailing_group_id: int
    risk_by_reward: ExactDecimal
    take_profit: ExactDecimal
    stop_loss: ExactDecimal
    is_active: Annotated[bool, Activation()] = True
    description: str | None
