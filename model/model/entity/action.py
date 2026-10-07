"""Action Entity."""

from decimal import Decimal
from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Action",
    description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The action's display name.",
        ),
        FieldDeclaration(
            name="action_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the action group that contains the action.",
        ),
        FieldDeclaration(
            name="asset_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the asset traded by the action.",
        ),
        FieldDeclaration(
            name="account_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the account used to execute the action.",
        ),
        FieldDeclaration(
            name="partial_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the Partial Group used by the action.",
        ),
        FieldDeclaration(
            name="trailing_group_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the Trailing Group used by the action.",
        ),
        FieldDeclaration(
            name="risk_by_reward",
            type=FieldType.decimal,
            nullable=False,
            description="Defines the numeric risk-to-reward value used by the action.",
        ),
        FieldDeclaration(
            name="take_profit",
            type=FieldType.decimal,
            nullable=False,
            description="Defines the Take Profit value used by the action.",
        ),
        FieldDeclaration(
            name="stop_loss",
            type=FieldType.decimal,
            nullable=False,
            description="Defines the Stop Loss value used by the action.",
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the action is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the action.",
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
    unique_constraints=(UniquenessConstraint(fields=("action_group_id", "name")),),
)


class Action(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    action_group_id: int = realize_field(DECLARATION, "action_group_id")
    asset_id: int = realize_field(DECLARATION, "asset_id")
    account_id: int = realize_field(DECLARATION, "account_id")
    partial_group_id: int = realize_field(DECLARATION, "partial_group_id")
    trailing_group_id: int = realize_field(DECLARATION, "trailing_group_id")
    risk_by_reward: Decimal = realize_field(DECLARATION, "risk_by_reward")
    take_profit: Decimal = realize_field(DECLARATION, "take_profit")
    stop_loss: Decimal = realize_field(DECLARATION, "stop_loss")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
