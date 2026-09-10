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


class TrailingGroup(DomainModel):
    """An independent group of the rules that manage Stop Loss and Take Profit during a trade."""

    logical_name = "Trailing Group"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    user_id: int = field(LogicalType.INTEGER, nullable=False, purpose="Identifies the user who owns the trailing group.")
    # unique is not stated by the definition and resolves from the Model name-field default.
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The trailing group's display name.")
    status: bool = field(
        LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the trailing group is active."
    )
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the trailing group.")

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
