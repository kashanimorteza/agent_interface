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
    unique_together,
)
from my_model._models.broker import Broker
from my_model._models.trading_platform import TradingPlatform


class Instance(DomainModel):
    """A connection through which the system reaches a Broker using a supported Trading Platform."""

    logical_name = "Instance"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    # unique is not stated by the definition and resolves from the Model name-field default.
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The instance's display name.")
    broker_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the broker connected through this instance."
    )
    trading_platform_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the trading platform used by this instance."
    )
    ip: str | None = field(
        LogicalType.STRING,
        nullable=True,
        purpose="Identifies the technical network address used to reach the Platform or Broker when required.",
    )
    username: str | None = field(
        LogicalType.STRING,
        nullable=True,
        purpose="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None | AwaitingGeneration = field(
        LogicalType.STRING,
        nullable=True,
        credential=True,
        at_rest=AtRestMode.ENCRYPTED,
        generation=GenerationMethod.SECURE,
        purpose="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None | AwaitingGeneration = field(
        LogicalType.STRING,
        nullable=True,
        credential=True,
        at_rest=AtRestMode.ENCRYPTED,
        generation=GenerationMethod.SECURE,
        purpose="Defines the technical API credential used to establish the Instance connection when required.",
    )
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the instance is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the instance.")

    declared_relationships = (
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
            role="trading platform",
            target=TradingPlatform,
            field="trading_platform_id",
            kind=RelationshipKind.USES,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Uses one Trading Platform through `trading_platform_id`.",
        ),
    )
    declared_rules = (
        # Evaluating it needs the selected platform's requirements and the moment of use.
        rule(
            "platform_required_connection_fields",
            ("trading_platform_id", "ip", "username", "password", "api_key"),
            RuleRequirement.APPLICATION_CONTEXT,
            statement=(
                "The Trading Platform selected through `trading_platform_id` defines which connection fields are "
                "required; every field it requires must be present before the Instance can be used."
            ),
        ),
        unique_together("broker_id", "name", statement="The combination of `broker_id` and `name` must be unique."),
    )
