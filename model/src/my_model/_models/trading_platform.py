from my_model._declarations import AwaitingGeneration, DomainModel, LogicalType, field


class TradingPlatform(DomainModel):
    """A supported trading API standard; its code selects the platform implementation to use."""

    logical_name = "Trading Platform"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    # unique is not stated by the definition and resolves from the Model name-field default.
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The platform's display name.")
    code: str = field(
        LogicalType.STRING,
        nullable=False,
        purpose=(
            "Identifies the implementation class the application must use for this trading platform, "
            "such as `binance` or `metatrader_5`."
        ),
    )
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the platform is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the platform.")
