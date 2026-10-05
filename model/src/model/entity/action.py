from decimal import Decimal
from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Action",
    description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
    fields=(
        identity(),
        FieldDeclaration(
            name="name",
            description="The action's display name.",
            type=FieldType.STRING,
            nullable=False,
        ),
        FieldDeclaration(
            name="action_group_id",
            description="Identifies the action group that contains the action.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="asset_id",
            description="Identifies the asset traded by the action.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="account_id",
            description="Identifies the account used to execute the action.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="partial_group_id",
            description="Identifies the Partial Group used by the action.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="trailing_group_id",
            description="Identifies the Trailing Group used by the action.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="risk_by_reward",
            description="Defines the numeric risk-to-reward value used by the action.",
            type=FieldType.DECIMAL,
            nullable=False,
        ),
        FieldDeclaration(
            name="take_profit",
            description="Defines the Take Profit value used by the action.",
            type=FieldType.DECIMAL,
            nullable=False,
        ),
        FieldDeclaration(
            name="stop_loss",
            description="Defines the Stop Loss value used by the action.",
            type=FieldType.DECIMAL,
            nullable=False,
        ),
        activity("Indicates whether the action is active."),
        FieldDeclaration(
            name="description",
            description="Describes the action.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(
        RelationDeclaration("action_group_id", "Action Group", "id"),
        RelationDeclaration("asset_id", "Asset", "id"),
        RelationDeclaration("account_id", "Account", "id"),
        RelationDeclaration("partial_group_id", "Partial Group", "id"),
        RelationDeclaration("trailing_group_id", "Trailing Group", "id"),
    ),
    unique_constraints=(
        UniqueConstraintDeclaration(
            (
                "action_group_id",
                "name",
            )
        ),
    ),
)


class Action(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    action_group_id: int = column(_DECLARATION, "action_group_id")
    asset_id: int = column(_DECLARATION, "asset_id")
    account_id: int = column(_DECLARATION, "account_id")
    partial_group_id: int = column(_DECLARATION, "partial_group_id")
    trailing_group_id: int = column(_DECLARATION, "trailing_group_id")
    risk_by_reward: Decimal = column(_DECLARATION, "risk_by_reward")
    take_profit: Decimal = column(_DECLARATION, "take_profit")
    stop_loss: Decimal = column(_DECLARATION, "stop_loss")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
