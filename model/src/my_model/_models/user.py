from my_model._declarations import AtRestMode, AwaitingGeneration, DomainModel, GenerationMethod, LogicalType, field


class User(DomainModel):
    """An independent user of the system; each user keeps its own, separate configuration."""

    logical_name = "User"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The user's display name.")
    username: str = field(LogicalType.STRING, nullable=False, purpose="The username used to identify the user.")
    password: str | AwaitingGeneration = field(
        LogicalType.STRING,
        nullable=False,
        credential=True,
        at_rest=AtRestMode.HASH,
        generation=GenerationMethod.SECURE,
        purpose="The password credential used by the user.",
    )
    api_key: str | AwaitingGeneration = field(
        LogicalType.STRING,
        nullable=False,
        credential=True,
        at_rest=AtRestMode.HASH,
        generation=GenerationMethod.SECURE,
        purpose="The API key assigned to the user.",
    )
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the user is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the user.")
