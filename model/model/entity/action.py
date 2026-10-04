"""The Action Entity."""

from decimal import Decimal

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import DecimalText, table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class Action(Entity, table=True):
    """The Action Entity."""

    __tablename__ = "Action"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("action_group_id", "name"),
    )

    declaration = Declaration(
        name="Action",
        description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        fields=(
            identity_declaration(),
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
            activity_declaration("Indicates whether the action is active."),
            FieldDeclaration(
                name="description",
                description="Describes the action.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="action_group_id",
                target_entity="Action Group",
                target_field="id",
            ),
            RelationDeclaration(
                local_field="asset_id", target_entity="Asset", target_field="id"
            ),
            RelationDeclaration(
                local_field="account_id", target_entity="Account", target_field="id"
            ),
            RelationDeclaration(
                local_field="partial_group_id",
                target_entity="Partial Group",
                target_field="id",
            ),
            RelationDeclaration(
                local_field="trailing_group_id",
                target_entity="Trailing Group",
                target_field="id",
            ),
        ),
        unique_constraints=(("action_group_id", "name"),),
    )

    id: int | None = identity_field()
    name: str = Field(description="The action's display name.")
    action_group_id: int = Field(
        foreign_key="ActionGroup.id",
        description="Identifies the action group that contains the action.",
    )
    asset_id: int = Field(
        foreign_key="Asset.id", description="Identifies the asset traded by the action."
    )
    account_id: int = Field(
        foreign_key="Account.id",
        description="Identifies the account used to execute the action.",
    )
    partial_group_id: int = Field(
        foreign_key="PartialGroup.id",
        description="Identifies the Partial Group used by the action.",
    )
    trailing_group_id: int = Field(
        foreign_key="TrailingGroup.id",
        description="Identifies the Trailing Group used by the action.",
    )
    risk_by_reward: Decimal = Field(
        sa_type=DecimalText,
        description="Defines the numeric risk-to-reward value used by the action.",
    )
    take_profit: Decimal = Field(
        sa_type=DecimalText,
        description="Defines the Take Profit value used by the action.",
    )
    stop_loss: Decimal = Field(
        sa_type=DecimalText,
        description="Defines the Stop Loss value used by the action.",
    )
    is_active: bool = activity_field("Indicates whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")
