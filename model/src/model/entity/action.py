"""The Action Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core._types import DecimalValue
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class Action(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Action",
        description=(
            "Defines how a position must be opened. An action "
            "selects the asset and account and provides the risk, "
            "Take Profit, Stop Loss, Partial Group, and Trailing "
            "Group settings that determine the position's "
            "parameters and execution behavior."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The action's display name.",
            ),
            FieldDeclaration(
                "action_group_id",
                "integer",
                nullable=False,
                description=("Identifies the action group that contains the action."),
            ),
            FieldDeclaration(
                "asset_id",
                "integer",
                nullable=False,
                description="Identifies the asset traded by the action.",
            ),
            FieldDeclaration(
                "account_id",
                "integer",
                nullable=False,
                description="Identifies the account used to execute the action.",
            ),
            FieldDeclaration(
                "partial_group_id",
                "integer",
                nullable=False,
                description="Identifies the Partial Group used by the action.",
            ),
            FieldDeclaration(
                "trailing_group_id",
                "integer",
                nullable=False,
                description="Identifies the Trailing Group used by the action.",
            ),
            FieldDeclaration(
                "risk_by_reward",
                "decimal",
                nullable=False,
                description=(
                    "Defines the numeric risk-to-reward value used by the action."
                ),
            ),
            FieldDeclaration(
                "take_profit",
                "decimal",
                nullable=False,
                description="Defines the Take Profit value used by the action.",
            ),
            FieldDeclaration(
                "stop_loss",
                "decimal",
                nullable=False,
                description="Defines the Stop Loss value used by the action.",
            ),
            activity("Indicates whether the action is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the action.",
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
        unique_constraints=(("action_group_id", "name"),),
    )

    id: int | None = None
    name: str
    action_group_id: int
    asset_id: int
    account_id: int
    partial_group_id: int
    trailing_group_id: int
    risk_by_reward: DecimalValue
    take_profit: DecimalValue
    stop_loss: DecimalValue
    is_active: bool = True
    description: str | None = None
