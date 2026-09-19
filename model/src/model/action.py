"""Action: how a position must be opened."""

from .account import Account
from .action_group import ActionGroup
from .asset import Asset
from .foundation import ExactDecimal, Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text
from .partial_group import PartialGroup
from .trailing_group import TrailingGroup


class Action(ModelFoundation):
    persistence = "persistent"
    relationships = (
        Relationship(field="action_group_id", reference=ActionGroup, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="asset_id", reference=Asset, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="account_id", reference=Account, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="partial_group_id", reference=PartialGroup, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="trailing_group_id", reference=TrailingGroup, reference_field="id", cardinality="many-to-one", optional=False),
    )
    unique_sets = (("action_group_id", "name"),)

    id: GeneratedId = None
    name: Text
    action_group_id: Integer
    asset_id: Integer
    account_id: Integer
    partial_group_id: Integer
    trailing_group_id: Integer
    risk_by_reward: ExactDecimal
    take_profit: ExactDecimal
    stop_loss: ExactDecimal
    is_active: Flag = True
    description: Text | None = None
