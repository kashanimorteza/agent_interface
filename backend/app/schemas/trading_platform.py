from pydantic import BaseModel, ConfigDict


class TradingPlatformCreate(BaseModel):
    name: str
    status: str
    description: str | None = None


class TradingPlatformUpdate(BaseModel):
    name: str
    status: str
    description: str | None = None


class TradingPlatformRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    description: str | None = None
