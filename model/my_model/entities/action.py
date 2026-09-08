"""The complete instruction for opening a position."""

from ..foundation import (
    Cardinality,
    FieldSpec,
    FieldType,
    InitialRecord,
    Relationship,
    define_entity,
)

Action = define_entity(
    name="Action",
    purpose=(
        "How a position is to be opened. An action selects what is traded and "
        "where, and carries the risk, take-profit, stop-loss, partial and trailing "
        "settings that decide the position's parameters and how it behaves once "
        "open."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The action's display name."),
        "action_group_id": FieldSpec(purpose="The action group that contains the action."),
        "asset_id": FieldSpec(purpose="The asset the action trades."),
        "account_id": FieldSpec(purpose="The account the action executes through."),
        "partial_group_id": FieldSpec(purpose="The partial group the action applies."),
        "trailing_group_id": FieldSpec(purpose="The trailing group the action applies."),
        "risk_by_reward": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The risk-to-reward value the action trades at.",
        ),
        "take_profit": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The take-profit value the action opens with.",
        ),
        "stop_loss": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The stop-loss value the action opens with.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the action."),
    },
    relationships=[
        Relationship(
            target="ActionGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="action_group",
            field="action_group_id",
        ),
        Relationship(
            target="Asset",
            cardinality=Cardinality.MANY_TO_ONE,
            role="asset",
            field="asset_id",
        ),
        Relationship(
            target="Account",
            cardinality=Cardinality.MANY_TO_ONE,
            role="account",
            field="account_id",
        ),
        Relationship(
            target="PartialGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="partial_group",
            field="partial_group_id",
        ),
        Relationship(
            target="TrailingGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="trailing_group",
            field="trailing_group_id",
        ),
    ],
    initial_records=[
        InitialRecord(
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
            }
        ),
    ],
)
