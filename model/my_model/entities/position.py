"""A position the system has created, executed or still pending."""

from ..foundation import (
    Cardinality,
    FieldSpec,
    FieldType,
    Relationship,
    define_entity,
)

Position = define_entity(
    name="Position",
    purpose=(
        "The complete record of a position the system created: where it was sent, "
        "what it came from, whether it has executed yet, and how far its protective "
        "and target levels have moved from the ones it opened with."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The position's display name."),
        "trading_platform_id": FieldSpec(purpose="The trading platform the position executes on."),
        "broker_id": FieldSpec(purpose="The broker the position executes through."),
        "account_id": FieldSpec(purpose="The trading account the position uses."),
        "trailing_group_id": FieldSpec(purpose="The trailing group applied to the position."),
        "partial_group_id": FieldSpec(purpose="The partial group applied to the position."),
        "action_group_id": FieldSpec(purpose="The action group the position belongs to."),
        "action_id": FieldSpec(purpose="The action the position was created from."),
        "date": FieldSpec(
            type=FieldType.DATETIME,
            nullable=False,
            purpose="The position's date and time.",
        ),
        "volume": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The position's trading volume.",
        ),
        "profit": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            default=0,
            purpose="The position's current profit or loss.",
        ),
        "is_executed": FieldSpec(
            type=FieldType.BOOLEAN,
            nullable=False,
            default=False,
            purpose="Indicates whether the position has been executed.",
        ),
        "order_type": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            purpose="The position's order type.",
        ),
        "base_tp": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The take-profit value the position opened with.",
        ),
        "base_sl": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The stop-loss value the position opened with.",
        ),
        "real_tp": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The position's current take-profit value.",
        ),
        "real_sl": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The position's current stop-loss value.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the position."),
    },
    relationships=[
        Relationship(
            target="TradingPlatform",
            cardinality=Cardinality.MANY_TO_ONE,
            role="trading_platform",
            field="trading_platform_id",
        ),
        Relationship(
            target="Broker",
            cardinality=Cardinality.MANY_TO_ONE,
            role="broker",
            field="broker_id",
        ),
        Relationship(
            target="Account",
            cardinality=Cardinality.MANY_TO_ONE,
            role="account",
            field="account_id",
        ),
        Relationship(
            target="TrailingGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="trailing_group",
            field="trailing_group_id",
        ),
        Relationship(
            target="PartialGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="partial_group",
            field="partial_group_id",
        ),
        Relationship(
            target="ActionGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="action_group",
            field="action_group_id",
        ),
        Relationship(
            target="Action",
            cardinality=Cardinality.MANY_TO_ONE,
            role="action",
            field="action_id",
        ),
    ],
)
