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


class Broker(DomainModel):
    """A supported broker, reached through Trading Platforms by way of its own Instances."""

    logical_name = "Broker"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    # unique is not stated by the definition and resolves from the Model name-field default.
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The broker's display name.")
    user_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the user who owns the broker configuration."
    )
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the broker is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the broker.")

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
    declared_rules = (unique_together("user_id", "name", statement="The combination of `user_id` and `name` must be unique."),)
