"""The Action Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class Action(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Action",
        description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                description="The action's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="action_group_id",
                description="Identifies the action group that contains the action.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="asset_id",
                description="Identifies the asset traded by the action.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="account_id",
                description="Identifies the account used to execute the action.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="partial_group_id",
                description="Identifies the Partial Group used by the action.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="trailing_group_id",
                description="Identifies the Trailing Group used by the action.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="risk_by_reward",
                description="Defines the numeric risk-to-reward value used by the action.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="take_profit",
                description="Defines the Take Profit value used by the action.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="stop_loss",
                description="Defines the Stop Loss value used by the action.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the action is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the action.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            Relation("action_group_id", "Action Group", "id"),
            Relation("asset_id", "Asset", "id"),
            Relation("account_id", "Account", "id"),
            Relation("partial_group_id", "Partial Group", "id"),
            Relation("trailing_group_id", "Trailing Group", "id"),
        ),
        unique_constraints=(
            ("action_group_id", "name"),
        ),
    )

    id: int | None = None
    name: str
    action_group_id: int
    asset_id: int
    account_id: int
    partial_group_id: int
    trailing_group_id: int
    risk_by_reward: Decimal
    take_profit: Decimal
    stop_loss: Decimal
    is_active: bool = True
    description: str | None = None
