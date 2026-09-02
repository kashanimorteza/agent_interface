from pydantic import BaseModel, ConfigDict


class TradingPlatformBase(BaseModel):
    name: str
    status: str
    description: str | None = None


class TradingPlatformCreate(TradingPlatformBase):
    pass


class TradingPlatformRead(TradingPlatformBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
