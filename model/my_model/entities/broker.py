"""A broker the system can work with through its trading platform."""

from ..foundation import (
    Cardinality,
    DomainRule,
    FieldSpec,
    FieldType,
    InitialRecord,
    Relationship,
    RuleScope,
    define_entity,
)

Broker = define_entity(
    name="Broker",
    purpose=(
        "A broker the system works with through the trading platform it uses. Any "
        "number of brokers can be configured, so the system is never tied to one."
    ),
    fields={
        "id": FieldSpec(),
        # Uniqueness belongs to the owner and the name together, so the name alone
        # is not unique.
        "name": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            unique=False,
            purpose="The broker's display name.",
        ),
        "user_id": FieldSpec(purpose="The user who owns the broker configuration."),
        "trading_platform_id": FieldSpec(purpose="The trading platform the broker uses."),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the broker."),
    },
    relationships=[
        Relationship(
            target="User",
            cardinality=Cardinality.MANY_TO_ONE,
            role="owner",
            field="user_id",
        ),
        Relationship(
            target="TradingPlatform",
            cardinality=Cardinality.MANY_TO_ONE,
            role="trading_platform",
            field="trading_platform_id",
        ),
    ],
    rules=[
        DomainRule(
            statement="A user has at most one broker of any given name.",
            scope=RuleScope.STORED_STATE,
            fields=("user_id", "name"),
        ),
    ],
    initial_records=[
        InitialRecord({"name": "FxPro", "user_id": 1, "trading_platform_id": 1}),
    ],
)
