"""The Action Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Action(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Action",
        description=(
            "Defines how a position must be opened. An action selects the asset and account and "
            "provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group "
            "settings that determine the position's parameters and execution behavior."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The action's display name.",
            ),
            FieldDeclaration(
                name="action_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the action group that contains the action.",
            ),
            FieldDeclaration(
                name="asset_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the asset traded by the action.",
            ),
            FieldDeclaration(
                name="account_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the account used to execute the action.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the Partial Group used by the action.",
            ),
            FieldDeclaration(
                name="trailing_group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the Trailing Group used by the action.",
            ),
            FieldDeclaration(
                name="risk_by_reward",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Defines the numeric risk-to-reward value used by the action.",
            ),
            FieldDeclaration(
                name="take_profit",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Defines the Take Profit value used by the action.",
            ),
            FieldDeclaration(
                name="stop_loss",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Defines the Stop Loss value used by the action.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the action is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the action.",
            ),
        ),
        relations=(
            Relation("action_group_id", "Action Group", "id"),
            Relation("asset_id", "Asset", "id"),
            Relation("account_id", "Account", "id"),
            Relation("partial_group_id", "Partial Group", "id"),
            Relation("trailing_group_id", "Trailing Group", "id"),
        ),
        unique_constraints=(UniquenessConstraint(("action_group_id", "name")),),
    )

    __tablename__ = "Action"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    name: str = mapped_field(declaration, "name")
    action_group_id: int = mapped_field(declaration, "action_group_id")
    asset_id: int = mapped_field(declaration, "asset_id")
    account_id: int = mapped_field(declaration, "account_id")
    partial_group_id: int = mapped_field(declaration, "partial_group_id")
    trailing_group_id: int = mapped_field(declaration, "trailing_group_id")
    risk_by_reward: Decimal = mapped_field(declaration, "risk_by_reward")
    take_profit: Decimal = mapped_field(declaration, "take_profit")
    stop_loss: Decimal = mapped_field(declaration, "stop_loss")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
