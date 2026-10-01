"""The Action Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Action",
    description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
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
        Relation(
            local_field="action_group_id",
            target_entity="Action Group",
            target_field="id",
        ),
        Relation(local_field="asset_id", target_entity="Asset", target_field="id"),
        Relation(local_field="account_id", target_entity="Account", target_field="id"),
        Relation(
            local_field="partial_group_id",
            target_entity="Partial Group",
            target_field="id",
        ),
        Relation(
            local_field="trailing_group_id",
            target_entity="Trailing Group",
            target_field="id",
        ),
    ),
    unique_constraints=(("action_group_id", "name"),),
    indexes=(),
)


class Action(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    name: str = Field(
        description="The action's display name.", **column_options(_DECLARATION, "name")
    )
    action_group_id: int = Field(
        description="Identifies the action group that contains the action.",
        **column_options(_DECLARATION, "action_group_id"),
    )
    asset_id: int = Field(
        description="Identifies the asset traded by the action.",
        **column_options(_DECLARATION, "asset_id"),
    )
    account_id: int = Field(
        description="Identifies the account used to execute the action.",
        **column_options(_DECLARATION, "account_id"),
    )
    partial_group_id: int = Field(
        description="Identifies the Partial Group used by the action.",
        **column_options(_DECLARATION, "partial_group_id"),
    )
    trailing_group_id: int = Field(
        description="Identifies the Trailing Group used by the action.",
        **column_options(_DECLARATION, "trailing_group_id"),
    )
    risk_by_reward: Decimal = Field(
        description="Defines the numeric risk-to-reward value used by the action.",
        **column_options(_DECLARATION, "risk_by_reward"),
    )
    take_profit: Decimal = Field(
        description="Defines the Take Profit value used by the action.",
        **column_options(_DECLARATION, "take_profit"),
    )
    stop_loss: Decimal = Field(
        description="Defines the Stop Loss value used by the action.",
        **column_options(_DECLARATION, "stop_loss"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the action is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the action.",
        **column_options(_DECLARATION, "description"),
    )
