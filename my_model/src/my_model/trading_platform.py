from pydantic import Field

from ._base import BaseModel


class TradingPlatform(BaseModel):
    """A supported trading API standard, independent of any specific exchange or broker."""

    id: int | None = Field(
        default=None, description="Generated once the Trading Platform is persisted."
    )
    name: str = Field(description="The platform's display name.")
    code: str = Field(
        description="Identifies the implementation the application must use for this trading platform."
    )
    status: bool = Field(
        default=True, description="Indicates whether the platform is active."
    )
    description: str | None = Field(default=None, description="Describes the platform.")
