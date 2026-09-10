from decimal import Decimal

from my_model._declarations import (
    AtRestMode,
    AwaitingGeneration,
    Cardinality,
    DomainModel,
    GenerationMethod,
    LogicalType,
    Participation,
    Relationship,
    RelationshipKind,
    RuleRequirement,
    field,
    rule,
)
from my_model._models.account_group import AccountGroup
from my_model._models.broker import Broker
from my_model._models.currency import Currency
from my_model._models.instance import Instance


class Account(DomainModel):
    """A funded trading account; its Instance owns the separate technical connection to the Broker."""

    logical_name = "Account"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The account's display name.")
    group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the account group that contains the account."
    )
    broker_id: int = field(LogicalType.INTEGER, nullable=False, purpose="Identifies the broker that owns the account.")
    instance_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the base currency used by the account."
    )
    username: str = field(
        LogicalType.STRING, nullable=False, purpose="The username identifier used to access the trading account."
    )
    password: str | AwaitingGeneration = field(
        LogicalType.STRING,
        nullable=False,
        credential=True,
        at_rest=AtRestMode.ENCRYPTED,
        generation=GenerationMethod.SECURE,
        purpose="The credential used to access the trading account.",
    )
    leverage: int = field(LogicalType.INTEGER, nullable=False, purpose="Defines the account's leverage multiplier.")
    balance: Decimal = field(
        LogicalType.DECIMAL, nullable=False, default=Decimal("0"), purpose="Stores the account's current balance."
    )
    account_type: str = field(
        LogicalType.STRING, nullable=False, purpose="Identifies the account model, such as `cfd` or `spread_betting`."
    )
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the account is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the account.")

    declared_relationships = (
        Relationship(
            role="account group",
            target=AccountGroup,
            field="group_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one Account Group through `group_id`.",
        ),
        Relationship(
            role="broker",
            target=Broker,
            field="broker_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one Broker through `broker_id`.",
        ),
        Relationship(
            role="instance",
            target=Instance,
            field="instance_id",
            kind=RelationshipKind.USES,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Uses one Instance through `instance_id`.",
        ),
        Relationship(
            role="base currency",
            target=Currency,
            field="base_currency_id",
            kind=RelationshipKind.USES,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Uses one Currency as its base currency through `base_currency_id`.",
        ),
    )
    declared_rules = (
        # Evaluating it needs the related Instance's credentials and the selected platform's requirements.
        rule(
            "credentials_not_duplicated_with_instance",
            ("username", "password", "instance_id"),
            RuleRequirement.APPLICATION_CONTEXT,
            statement=(
                "Instance credentials authenticate the technical Platform or Broker connection; Account credentials "
                "authenticate this specific trading account. The same credential must not be duplicated across both "
                "Models unless the selected Trading Platform explicitly requires it in both roles."
            ),
        ),
        # Evaluating it needs the stored Instance record's Broker.
        rule(
            "instance_belongs_to_account_broker",
            ("instance_id", "broker_id"),
            RuleRequirement.STORED_STATE,
            statement="The Instance selected through `instance_id` must belong to the Account's Broker.",
        ),
    )
