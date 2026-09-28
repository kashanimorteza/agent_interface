"""The Action Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class Action(Entity, table=True):
    """The Action Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Action",
        description="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
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
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
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
        unique_constraints=(UniqueConstraint(fields=("action_group_id", "name")),),
    )

    __table_args__ = (TableUniqueConstraint("action_group_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
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
