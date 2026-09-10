from decimal import Decimal

from my_model._declarations import (
    AwaitingGeneration,
    Cardinality,
    DomainModel,
    LogicalType,
    Participation,
    Relationship,
    RelationshipKind,
    field,
)
from my_model._models.account import Account
from my_model._models.action_group import ActionGroup
from my_model._models.asset import Asset
from my_model._models.partial_group import PartialGroup
from my_model._models.trailing_group import TrailingGroup


class Action(DomainModel):
    """How a position must be opened: asset, account, risk, targets, and the Partial and Trailing Groups used."""

    logical_name = "Action"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The action's display name.")
    action_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the action group that contains the action."
    )
    asset_id: int = field(LogicalType.INTEGER, nullable=False, purpose="Identifies the asset traded by the action.")
    account_id: int = field(LogicalType.INTEGER, nullable=False, purpose="Identifies the account used to execute the action.")
    partial_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the Partial Group used by the action."
    )
    trailing_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the Trailing Group used by the action."
    )
    risk_by_reward: Decimal = field(
        LogicalType.DECIMAL, nullable=False, purpose="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = field(
        LogicalType.DECIMAL, nullable=False, purpose="Defines the Take Profit value used by the action."
    )
    stop_loss: Decimal = field(LogicalType.DECIMAL, nullable=False, purpose="Defines the Stop Loss value used by the action.")
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the action is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the action.")

    declared_relationships = (
        Relationship(
            role="action group",
            target=ActionGroup,
            field="action_group_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one Action Group through `action_group_id`.",
        ),
        Relationship(
            role="asset",
            target=Asset,
            field="asset_id",
            kind=RelationshipKind.USES,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Uses one Asset through `asset_id`.",
        ),
        Relationship(
            role="account",
            target=Account,
            field="account_id",
            kind=RelationshipKind.USES,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Uses one Account through `account_id`.",
        ),
        Relationship(
            role="partial group",
            target=PartialGroup,
            field="partial_group_id",
            kind=RelationshipKind.USES,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Uses one Partial Group through `partial_group_id`.",
        ),
        Relationship(
            role="trailing group",
            target=TrailingGroup,
            field="trailing_group_id",
            kind=RelationshipKind.USES,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Uses one Trailing Group through `trailing_group_id`.",
        ),
    )
