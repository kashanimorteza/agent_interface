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
from my_model._models.user import User


class Currency(DomainModel):
    """A currency the trading system can use, with its code, symbol, region, and monetary precision."""

    logical_name = "Currency"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    user_id: int = field(LogicalType.INTEGER, nullable=False, purpose="Identifies the user who owns this currency.")
    # unique is not stated by the definition and resolves from the Model name-field default.
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The currency's full name.")
    code: str = field(
        LogicalType.STRING,
        nullable=False,
        size=3,
        purpose="The currency's standard three-letter code, such as `USD` or `EUR`.",
    )
    symbol: str | None = field(
        LogicalType.STRING, nullable=True, purpose="The currency's display symbol, such as `$`, `€`, or `£`."
    )
    country: str | None = field(
        LogicalType.STRING, nullable=True, purpose="Identifies the country or region associated with the currency."
    )
    decimal_digits: int = field(
        LogicalType.INTEGER,
        nullable=False,
        default=2,
        purpose="Defines the number of decimal digits normally used for monetary values in the currency.",
    )
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the currency is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the currency.")

    declared_relationships = (
        Relationship(
            role="user",
            target=User,
            field="user_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one User through `user_id`.",
        ),
    )
    declared_rules = (unique_together("user_id", "code", statement="The combination of `user_id` and `code` must be unique."),)
