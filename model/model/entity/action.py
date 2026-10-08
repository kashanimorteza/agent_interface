"""The Action Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Action(Foundation, table=True):
    __tablename__ = "Action"
    declaration: ClassVar[Declaration] = Declaration(
        name="Action",
        description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "name",
                FieldType.string,
                False,
                description="The action's display name.",
            ),
            FieldDeclaration(
                "action_group_id",
                FieldType.integer,
                False,
                description="Identifies the action group that contains the action.",
            ),
            FieldDeclaration(
                "asset_id",
                FieldType.integer,
                False,
                description="Identifies the asset traded by the action.",
            ),
            FieldDeclaration(
                "account_id",
                FieldType.integer,
                False,
                description="Identifies the account used to execute the action.",
            ),
            FieldDeclaration(
                "partial_group_id",
                FieldType.integer,
                False,
                description="Identifies the Partial Group used by the action.",
            ),
            FieldDeclaration(
                "trailing_group_id",
                FieldType.integer,
                False,
                description="Identifies the Trailing Group used by the action.",
            ),
            FieldDeclaration(
                "risk_by_reward",
                FieldType.decimal,
                False,
                description="Defines the numeric risk-to-reward value used by the action.",
            ),
            FieldDeclaration(
                "take_profit",
                FieldType.decimal,
                False,
                description="Defines the Take Profit value used by the action.",
            ),
            FieldDeclaration(
                "stop_loss",
                FieldType.decimal,
                False,
                description="Defines the Stop Loss value used by the action.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the action is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
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
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    name: str = realize_field(declaration, "name")
    action_group_id: int = realize_field(declaration, "action_group_id")
    asset_id: int = realize_field(declaration, "asset_id")
    account_id: int = realize_field(declaration, "account_id")
    partial_group_id: int = realize_field(declaration, "partial_group_id")
    trailing_group_id: int = realize_field(declaration, "trailing_group_id")
    risk_by_reward: Decimal = realize_field(declaration, "risk_by_reward")
    take_profit: Decimal = realize_field(declaration, "take_profit")
    stop_loss: Decimal = realize_field(declaration, "stop_loss")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
