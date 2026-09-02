from pydantic import BaseModel, ConfigDict


class BrokerCreate(BaseModel):
    name: str
    trading_platform_id: int
    status: str
    description: str | None = None


class BrokerUpdate(BaseModel):
    name: str
    trading_platform_id: int
    status: str
    description: str | None = None


class BrokerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    trading_platform_id: int
    status: str
    description: str | None = None
