from decimal import Decimal
from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core._columns import DecimalText
from model.core.declaration import Declaration, FieldDeclaration, Relation


class Action(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("action_group_id", "name"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Action",
        "Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("name", "The action's display name.", "string", False),
            FieldDeclaration(
                "action_group_id", "Identifies the action group that contains the action.", "integer", False
            ),
            FieldDeclaration("asset_id", "Identifies the asset traded by the action.", "integer", False),
            FieldDeclaration("account_id", "Identifies the account used to execute the action.", "integer", False),
            FieldDeclaration("partial_group_id", "Identifies the Partial Group used by the action.", "integer", False),
            FieldDeclaration(
                "trailing_group_id", "Identifies the Trailing Group used by the action.", "integer", False
            ),
            FieldDeclaration(
                "risk_by_reward", "Defines the numeric risk-to-reward value used by the action.", "decimal", False
            ),
            FieldDeclaration("take_profit", "Defines the Take Profit value used by the action.", "decimal", False),
            FieldDeclaration("stop_loss", "Defines the Stop Loss value used by the action.", "decimal", False),
            FieldDeclaration(
                "is_active", "Indicates whether the action is active.", "boolean", False, has_default=True, default=True
            ),
            FieldDeclaration("description", "Describes the action.", "string", True),
        ),
        "id",
        relations=(
            Relation("action_group_id", "Action Group", "id"),
            Relation("asset_id", "Asset", "id"),
            Relation("account_id", "Account", "id"),
            Relation("partial_group_id", "Partial Group", "id"),
            Relation("trailing_group_id", "Trailing Group", "id"),
        ),
        unique_constraints=(
            (
                "action_group_id",
                "name",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    name: str = Field(description="The action's display name.")
    action_group_id: int = Field(
        foreign_key="ActionGroup.id", description="Identifies the action group that contains the action."
    )
    asset_id: int = Field(foreign_key="Asset.id", description="Identifies the asset traded by the action.")
    account_id: int = Field(foreign_key="Account.id", description="Identifies the account used to execute the action.")
    partial_group_id: int = Field(
        foreign_key="PartialGroup.id", description="Identifies the Partial Group used by the action."
    )
    trailing_group_id: int = Field(
        foreign_key="TrailingGroup.id", description="Identifies the Trailing Group used by the action."
    )
    risk_by_reward: Decimal = Field(
        sa_type=DecimalText, description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Field(sa_type=DecimalText, description="Defines the Take Profit value used by the action.")
    stop_loss: Decimal = Field(sa_type=DecimalText, description="Defines the Stop Loss value used by the action.")
    is_active: bool = Field(default=True, description="Indicates whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")
