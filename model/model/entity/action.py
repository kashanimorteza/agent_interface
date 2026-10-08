"""Action Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Action(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Action",
        description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        primary_key="id",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.integer,
                nullable=False,
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
        relations=(
            Relation(
                local_field="action_group_id",
                target_entity="Action Group",
                target_field="id",
            ),
            Relation(local_field="asset_id", target_entity="Asset", target_field="id"),
            Relation(
                local_field="account_id", target_entity="Account", target_field="id"
            ),
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
    )
    __tablename__ = "Action"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    name: str = storage.field(declaration, "name")
    action_group_id: int = storage.field(declaration, "action_group_id")
    asset_id: int = storage.field(declaration, "asset_id")
    account_id: int = storage.field(declaration, "account_id")
    partial_group_id: int = storage.field(declaration, "partial_group_id")
    trailing_group_id: int = storage.field(declaration, "trailing_group_id")
    risk_by_reward: Decimal = storage.field(declaration, "risk_by_reward")
    take_profit: Decimal = storage.field(declaration, "take_profit")
    stop_loss: Decimal = storage.field(declaration, "stop_loss")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
