"""The Action Model."""

from decimal import Decimal
from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType, RelationshipSpec


class Action(Model):
    """Defines how a position must be opened. An action selects the asset and account and provides the
    risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the
    position's parameters and execution behavior.
    """

    logical_key: ClassVar[str] = "action"
    logical_purpose: ClassVar[str] = (
        "Defines how a position must be opened. An action selects the asset and account and provides the "
        "risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the "
        "position's parameters and execution behavior."
    )
    logical_relationships: ClassVar[tuple[RelationshipSpec, ...]] = (
        RelationshipSpec(name="action_group", type="belongs_to", target="action_group", field="action_group_id"),
        RelationshipSpec(name="asset", type="uses", target="asset", field="asset_id"),
        RelationshipSpec(name="account", type="uses", target="account", field="account_id"),
        RelationshipSpec(name="partial_group", type="uses", target="partial_group", field="partial_group_id"),
        RelationshipSpec(name="trailing_group", type="uses", target="trailing_group", field="trailing_group_id"),
    )
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {
            "name": "Default",
            "action_group_id": 1,
            "asset_id": 1,
            "account_id": 1,
            "partial_group_id": 1,
            "trailing_group_id": 1,
            "risk_by_reward": 1,
            "take_profit": 1,
            "stop_loss": 1,
        },
    )

    id: Annotated[
        int | None,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            auto_increment=True,
            primary_key=True,
        ),
    ] = None
    name: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="The action's display name.",
        ),
    ]
    action_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the action group that contains the action.",
        ),
    ]
    asset_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the asset traded by the action.",
        ),
    ]
    account_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the account used to execute the action.",
        ),
    ]
    partial_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the Partial Group used by the action.",
        ),
    ]
    trailing_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the Trailing Group used by the action.",
        ),
    ]
    risk_by_reward: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Defines the numeric risk-to-reward value used by the action.",
        ),
    ]
    take_profit: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Defines the Take Profit value used by the action.",
        ),
    ]
    stop_loss: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Defines the Stop Loss value used by the action.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the action is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the action.",
        ),
    ] = None
