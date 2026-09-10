from my_model._declarations import (
    AwaitingGeneration,
    Cardinality,
    DomainModel,
    LogicalType,
    Participation,
    Relationship,
    RelationshipKind,
    field,
    unique_together,
)
from my_model._models.broker import Broker


class Asset(DomainModel):
    """A tradable asset a broker provides, identified by symbol and category."""

    logical_name = "Asset"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    broker_id: int = field(LogicalType.INTEGER, nullable=False, purpose="Identifies the broker that provides this asset.")
    # unique is not stated by the definition and resolves from the Model name-field default.
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The asset's display name.")
    symbol: str = field(
        LogicalType.STRING,
        nullable=False,
        purpose="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
    )
    category: str = field(
        LogicalType.STRING,
        nullable=False,
        purpose="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
    )
    point_size: float = field(
        LogicalType.FLOAT, nullable=False, default=0.0, purpose="Stores the size of one point for the asset."
    )
    digits: int = field(
        LogicalType.INTEGER,
        nullable=False,
        default=0,
        purpose="Stores the number of decimal digits used for the asset's price.",
    )
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the asset is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the asset.")

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
    )
    declared_rules = (
        unique_together("broker_id", "name", statement="The combination of `broker_id` and `name` must be unique."),
        unique_together("broker_id", "symbol", statement="The combination of `broker_id` and `symbol` must be unique."),
    )
